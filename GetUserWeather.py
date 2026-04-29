# Name: Terry Wayne Smith
# Date: 11-4-2024
# Class: ITSE 1402 Computer Programming
# Purpose: This program fetches and displays weather alerts for specific locations. It allows the user to get Local Weather from my Weather Station, City Weather in Texas, Local IP and State Weather alerts.
# 
# This Module will get User requested weather


import requests
from bs4 import BeautifulSoup

def quit_program():
    print("Are you not enjoying my program??...Goodbye")
    return False

def city():
    global last_known_city
    city_name = input("Please Enter the city you want weather from: Or press Q/Quit to Exit Program ")

    if city_name.lower() == "q" or city_name.lower() == "quit":
        return quit_program()
    elif city_name == "":
        return None
    else:
        print("You have entered", city_name)
        last_known_city = city_name
        return city_name


def get_weather(city_name): # Get User Requested Weather 
    url = f"https://www.wunderground.com/weather/us/tx/{city_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    temperature = soup.find(class_="current-temp").get_text()
    humidity = soup.find(class_= "wu-unit-humidity").get_text() 
    humidity = humidity.replace("°", "").strip()
    wind_chill = soup.find(class_="temp").get_text()
    wind_speed = soup.find(class_="wind-speed").get_text()
    weather_data ={"temperature" : temperature, "wind_chill": wind_chill, "humidity" : humidity, "wind_speed" : wind_speed}
    return weather_data #wind_unit, wind_direction

def user_weather(city_name):
    weather_data = get_weather(city_name)
    temperature = weather_data["temperature"]
    humidity = weather_data["humidity"]
    wind_chill = weather_data["wind_chill"]
    wind_speed = weather_data["wind_speed"]
    print(f"The temperature in {city_name} is {temperature}  Feels Like Temp {wind_chill} Humidity is {humidity} Wind speed is {wind_speed} mph")
        
    with open("user_weather.html", "w") as file:
        file.write(f"The temperature in {city_name} TX is {temperature}\n")
        file.write(f"Feels Like: {wind_chill} F\n")
        file.write(f"Humidity: {humidity}\n")
        file.write(f"Wind speed: {wind_speed} mph\n")
        

