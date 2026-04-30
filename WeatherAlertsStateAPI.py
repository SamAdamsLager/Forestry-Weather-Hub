# Name: Terry Wayne Smith
# Date: 05-07-2025
# Class: ITSE-1411-V01-Beginning Web Page Programming
# Purpose: This program fetches and displays weather alerts for specific locations. It allows the user to get Local Weather from my Weather Station, City Weather in Texas, Local IP and State Weather alerts.

import requests
import json
from datetime import datetime

def fetch_state_alerts(state_input):
    valid_states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    alerts_list = []
    current_time = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    error_message = None
    processed_state = None

    if isinstance(state_input, str):
        processed_state = state_input.strip().upper()
        if processed_state not in valid_states:
            error_message = f"Invalid state abbreviation '{state_input}'. Please use a valid 2-letter code."
            processed_state = None
    else:
         error_message = "Invalid input: State abbreviation must be a string."
         processed_state = None

    if processed_state and not error_message:
        try:
            alert_api_url = f"https://api.weather.gov/alerts/active?area={processed_state}"
            headers = {'User-Agent': '(MyWeatherApp, myemail@example.com)'}
            response = requests.get(alert_api_url, headers=headers, timeout=15)
            response.raise_for_status()
            alert_data = response.json()

            if "features" in alert_data and alert_data["features"]:
                for alert in alert_data['features']:
                    properties = alert.get('properties', {})
                    alerts_list.append({
                        'headline': properties.get('headline', 'N/A'),
                        'areaDesc': properties.get('areaDesc', 'N/A'),
                        'description': properties.get('description', 'N/A')
                    })

        except requests.exceptions.Timeout:
            print(f"Network timeout fetching state alerts for {processed_state}.")
            error_message = "A network request timed out."
        except requests.exceptions.RequestException as e:
            print(f"Network error fetching state alerts for {processed_state}: {e}")
            error_message = "Network error occurred while fetching data."
        except Exception as e:
            print(f"An unexpected error occurred processing state {processed_state}: {e}")
            error_message = "An unexpected processing error occurred."

    return {
        "state_req": state_input,
        "state_proc": processed_state,
        "current_time": current_time,
        "alerts": alerts_list,
        "error": error_message
    }