# Name: Terry Wayne Smith
# Date: 05-07-2025
# Class: ITSE-1411-V01-Beginning Web Page Programming
# Purpose: Fetches local‑station weather and writes a full HTML page.

from datetime import datetime, timedelta               
from pathlib import Path                     
from playwright.sync_api import sync_playwright, Error

_last_fetch = None
_cached_data = None

# ------------------------------------------------------------------ fetch
def fetch_weather():
    url = "https://www.wunderground.com/dashboard/pws/KTXMCALL89"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60_000)
            page.wait_for_selector(".main-temp .wu-value", timeout=60_000)

            def safe(sel):
                try:
                    return page.locator(sel).inner_text().strip()
                except:
                    return "N/A"

            data = {
                "temperature": safe(".main-temp .wu-value"),
                "wind_chill":  safe(".feels-like-temp.weather__header .wu-value"),
                "wind_speed":  safe(".weather__wind-gust .wu-unit-speed .wu-value"),
                "wind_dial":   safe("div.wind-dial__container .text-wrapper .text-bold"),
            }
            browser.close()
            return data

    except Error as e:
        print("Playwright error:", e)
        return {k: "N/A" for k in
                ["temperature", "wind_chill", "wind_speed", "wind_dial"]}
    

"""Return cached weather for 30 min, refresh after 30"""
def fetch_weather_cached():
    global _last_fetch, _cached_data
    if _last_fetch and datetime.now() - _last_fetch < timedelta(minutes=30):
        return _cached_data
    
    _cached_data = fetch_weather()     # Playwright scrape
    _last_fetch  = datetime.now()
    return _cached_data
    

    

def local_weather():
    weather = fetch_weather_cached()

    # ---- timestamp -------------------------------------------------------
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # ----------------------------------------------------------------------

    weather_block = f"""
        <p><strong>Last updated:</strong> {now}</p>
        <ul>
          <li><strong>Temperature:</strong> {weather['temperature']}°F</li>
          <li><strong>Feels Like:</strong> {weather['wind_chill']}°F</li>
          <li><strong>Wind Speed:</strong> {weather['wind_speed']} mph</li>
          <li><strong>Wind Direction:</strong> {weather['wind_dial']}</li>
        </ul>
    """

    tpl   = Path("templates/_local_weather_template.html")
    final = Path("static/html/live_local_weather.html")

    html  = tpl.read_text(encoding="utf-8").replace("{{WEATHER_BLOCK}}", weather_block)
    final.write_text(html, encoding="utf-8")
