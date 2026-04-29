# Name: Terry Wayne Smith
# Date: 11-4-2024
# Class: ITSE 1402 Computer Programming
# Purpose: This program fetches and displays weather alerts for specific locations. It allows the user to get Local Weather from my Weather Station, City Weather in Texas, Local IP and State Weather alerts.

import requests
from datetime import datetime

def fetch_ip_alerts():
    ip_address = requests.get("http://api.ipify.org").text
    print(ip_address)

    geo_data = requests.get(f"http://ip-api.com/json/{ip_address}").json()
    print(geo_data)

    lat = geo_data["lat"]
    lon = geo_data["lon"]
    city = geo_data["city"]
    state = geo_data["regionName"]
    print (lat)
    print (lon)

    response = requests.get(f"https://api.weather.gov/alerts?point={lat},{lon}").json()
    current_time = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    print(f"Alerts: {len(response["features"])}")

    with open("local_alerts.html", "w") as file:
        if "features" in response and response["features"]:
            for alert in response["features"]:
                file.write(f"<h1>{alert["properties"]["headline"]}</h1>")
                file.write(f"<h3>{alert["properties"]["areaDesc"]}</h3>")
                file.write(f"<p>{alert["properties"]["description"]}</p>")
        else:
            file.write("<html><head><title>Local Weather Alerts</title></head><body>")
            file.write("<h1>NO ACTIVE ALERTS</h1>")
            file.write(f"<h1>State: {state}</h1>")
            file.write(f"<h1>City: {city}</h1>")
            file.write(f"<p>Time: {current_time}</p>")
            file.write("</body></html>")
    file.close()