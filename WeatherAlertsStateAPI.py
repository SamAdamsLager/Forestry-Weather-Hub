# Name: Terry Wayne Smith
# Date: 11-4-2024
# Class: ITSE 1402 Computer Programming
# Purpose: This program fetches and displays weather alerts for specific locations. It allows the user to get Local Weather from my Weather Station, City Weather in Texas, Local IP and State Weather alerts.

import requests
import json    
from datetime import datetime

def fetch_state_alerts(state):
    # List of valid state abbreviations
    valid_states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

    # Prompt user for state abbreviation
   # state = input("""Enter the State you want weather alerts from,
#Use 2 letter abbreviation, ex TX for Texas FL for Florida """).upper()

    # Validate input
    if state not in valid_states:
        print("Invalid state abbreviation. Please enter a valid 2 letter state abbreviation (e.g., TX, FL).")
    else: 
        response = requests.get(f"https://api.weather.gov/alerts/active?area={state}").json()
        current_time = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

    
    

    if "features" in response and response["features"]:
        for alert in response["features"]:
            print(alert["properties"]["areaDesc"])
            print(alert["properties"]["headline"])
            print(alert["properties"]["description"])
            print("\n**********\n") 

        file = open("state_alerts.html", "w")
        for x in response["features"]:
            file.write(f"<h1>{x["properties"]["headline"]}</h1>")
            file.write(f"<h3>{x["properties"]["areaDesc"]}</h3>")
            file.write(f"<p>{x["properties"]["description"]}</p>")
        file.close()
        print("Please check state_alerts.html in your local directory for html file")
    else:
        file = open("state_alerts.html", "w")
        file.write(f"<h1><head><title>State Weathe Alerts</title></head><body>")
        file.write("<h1>No Active Alerts</h1>")
        file.write("</body></html>")
        file.write(f"<p>State: {state}</p>")
        file.write(f"<p>Time: {current_time}</p>")
        file.close()
        print("No active alerts for the specified state. ")
