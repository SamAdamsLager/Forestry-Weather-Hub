# Name: Terry Wayne Smith
# Date: 05-07-2025
# Class: ITSE-1411-V01-Beginning Web Page Programming
# Purpose: This program fetches and displays weather alerts for specific locations. It allows the user to get Local Weather from my Weather Station, City Weather in Texas, Local IP and State Weather alerts.

import requests
from datetime import datetime

def fetch_ip_alerts(visitor_ip):
    ip_address = None
    geo_data = {}
    alerts_list = []
    city = "N/A"
    state = "N/A"
    lat = None
    lon = None
    current_time = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    error_message = None

    try:
        geo_response = requests.get(f"http://ip-api.com/json/{visitor_ip}", timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if geo_data.get("status") == "success":
            lat = geo_data.get("lat")
            lon = geo_data.get("lon")
            city = geo_data.get("city", "N/A")
            state = geo_data.get("regionName", "N/A")

            if lat is not None and lon is not None:
                alert_api_url = f"https://api.weather.gov/alerts/active?point={lat},{lon}"
                headers = {'User-Agent': '(MyWeatherApp, myemail@example.com)'}
                alert_response = requests.get(alert_api_url, headers=headers, timeout=15)
                alert_response.raise_for_status()
                alert_data = alert_response.json()

                if "features" in alert_data and alert_data["features"]:
                    for alert in alert_data['features']:
                        properties = alert.get('properties', {})
                        alerts_list.append({
                            'headline': properties.get('headline', 'N/A'),
                            'areaDesc': properties.get('areaDesc', 'N/A'),
                            'description': properties.get('description', 'N/A')
                        })
            else:
                 error_message = "Could not determine latitude/longitude from IP."

        else:
            error_message = f"Geolocation lookup failed: {geo_data.get('message', 'Unknown error')}"

    except requests.exceptions.Timeout:
        print(f"Network timeout fetching IP/Geo/Alert data.")
        error_message = "A network request timed out."
    except requests.exceptions.RequestException as e:
        print(f"Network error fetching IP/Geo/Alert data: {e}")
        error_message = "Network error occurred while fetching data."
    except Exception as e:
        print(f"An unexpected error occurred in fetch_ip_alerts: {e}")
        error_message = "An unexpected processing error occurred."

    return {
        "city": city,
        "state": state,
        "current_time": current_time,
        "alerts": alerts_list,
        "error": error_message
    }