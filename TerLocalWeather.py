# Name: Terry Wayne Smith
# Date: 11-4-2024
# Class: ITSE 1402 Computer Programming
# Purpose: This program fetches and displays weather alerts for specific locations. It allows the user to get Local Weather from my Weather Station, City Weather in Texas, Local IP and State Weather alerts.


import requests
from bs4 import BeautifulSoup

def fetch_weather(): # Fetch My McAllen Weather Station 
    url = "https://www.wunderground.com/dashboard/pws/KTXMCALL89"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    temperature = soup.find(class_="current-temp").get_text()
    humidity = soup.find(class_= "wu-unit-humidity").get_text() 
    humidity = humidity.replace("°", "").strip()
    wind_chill = soup.find(class_="feels-like-temp weather__header").get_text()
    wind_speed = soup.find(class_="weather__text").get_text()
    wind_speed = wind_speed.replace ("°", "").strip()
    wind_dial = soup.find(class_="wind-dial__container").get_text()
    weather_data ={"temperature" : temperature, "wind_chill": wind_chill, "humidity" : humidity, "wind_speed" : wind_speed, "wind_dial" : wind_dial}
    return weather_data #wind_unit, wind_direction

def local_weather():
    weather_data = fetch_weather()
    temperature = weather_data["temperature"]
    humidity = weather_data["humidity"]
    wind_chill = weather_data["wind_chill"]
    wind_speed = weather_data["wind_speed"]
    wind_dial = weather_data["wind_dial"]
    print(f"The temperature in McAllen TX is {temperature}  {wind_chill} Humidity is {humidity} Wind speed is {wind_speed}  from the {wind_dial}")

    with open("local_weather.html", "w") as file:
        file.write(f"The temperature in McAllen TX is {temperature}\n")
        file.write(f"Feels Like: {wind_chill}\n")
        file.write(f"Humidity: {humidity}\n")
        file.write(f"Wind speed: {wind_speed}\n")
        file.write(f"Wind direction: {wind_dial}\n")
    
        