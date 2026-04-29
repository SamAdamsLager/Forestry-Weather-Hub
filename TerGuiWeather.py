# Name: Terry Wayne Smith
# Date: 11-4-2024
# Class: ITSE 1402 Computer Programming
# Purpose: This program fetches and displays weather alerts for specific locations. It allows the user to get Local Weather from my Weather Station, City Weather in Texas, Local IP and State Weather alerts.


import tkinter as tk
import re
from tkinter import simpledialog
from tkinter import scrolledtext
import TerLocalWeather
import GetUserWeather
import IPaddressAlertsAPI
import WeatherAlertsStateAPI
from bs4 import BeautifulSoup
from datetime import datetime

local_weather_text = None


window = tk.Tk()
window.title("Ter's Weather Program")
window.geometry("600x400")

label = tk.Label(text = "Ter's Weather Program")
label.pack(pady=10) 

def prompt_for_city():
    city_name = simpledialog.askstring("City Name", "Enter the city you want weather for:")
    if city_name:
        GetUserWeather.user_weather(city_name)
        show_city_weather()
        
        
def prompt_for_state():
    state = simpledialog.askstring("State Abbreviation", "Enter the State you want weather alerts for (e.g., TX, FL):").upper()
    if state:
        WeatherAlertsStateAPI.fetch_state_alerts(state)
        show_state_alerts(state)


def show_local_weather():
    global local_weather_text
    TerLocalWeather.local_weather()  # Calling function from module
    try:
        with open("local_weather.html", "r") as file:
            weather_content = file.read()

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not local_weather_text:
            weather_window = tk.Toplevel(window)
            weather_window.title("Local Weather")
            weather_window.geometry("600x400")

            local_weather_text = scrolledtext.ScrolledText(weather_window, wrap=tk.WORD)
            local_weather_text.pack(expand=True, fill=tk.BOTH)
        else:
            local_weather_text.configure(state="normal")
            local_weather_text.delete(1.0, tk.END)  # Clear existing content

        local_weather_text.insert(tk.END, f"Last updated: {current_time}\n\n{weather_content}")
        local_weather_text.configure(state="disabled")
    except FileNotFoundError:
        print("Error: local_weather.html file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

   
def show_city_weather():
    try:
        with open("user_weather.html", "r") as file:
            weather_content = file.read()        
    
        weather_window = tk.Toplevel(window)
        weather_window.title("City Weather for Texas")
        weather_window.geometry("600x400")

        text_area = scrolledtext.ScrolledText(weather_window, wrap=tk.WORD)
        text_area.pack(expand=True,fill=tk.BOTH)
        text_area.insert(tk.END, weather_content)
        text_area.configure(state="disabled")
    except FileNotFoundError:
        print("Error: user_weather.html file not found")
    except Exception as e:
        print(f"An error has occurred: {e}")
    
def show_ip_alerts(): #IP alerts text box
    IPaddressAlertsAPI.fetch_ip_alerts()
    try:
        with open("local_alerts.html", "r", encoding="utf-8") as file:
            html_content = file.read()
    
    # Use BeautifulSoup to parse HTML and extract plain text
        soup = BeautifulSoup(html_content, "html.parser")
        plain_text = soup.get_text(separator="\n")  # Extract text with newlines between tags

        weather_window = tk.Toplevel(window)
        weather_window.title("IP Alerts for your area")
        weather_window.geometry("600x400")

        text_area = scrolledtext.ScrolledText(weather_window, wrap=tk.WORD)
        text_area.pack(expand=True, fill=tk.BOTH)
        text_area.insert(tk.END, plain_text)  # Use plain_text to ensure HTML tags are removed
        text_area.configure(state="disabled")
    except FileNotFoundError:
        print("Error: local-weather.html. file not found")
    except Exception as e:
        print(f"An error has occurred: {e}")
        
def show_state_alerts(state):
    try:
        with open("state_alerts.html", "r", encoding="utf-8") as file:
            html_content = file.read()
    
    # Use BeautifulSoup to parse HTML and extract plain text
        soup = BeautifulSoup(html_content, "html.parser")
        plain_text = soup.get_text(separator="\n")  # Extract text with newlines between tags

        weather_window = tk.Toplevel(window)
        weather_window.title(f"Alerts for {state}")
        weather_window.geometry("600x400")

        text_area = scrolledtext.ScrolledText(weather_window, wrap=tk.WORD)
        text_area.pack(expand=True, fill=tk.BOTH)
        text_area.insert(tk.END, plain_text)  # Use plain_text to ensure HTML tags are removed
        text_area.configure(state="disabled")
    except FileNotFoundError:
        print("Error: local-weather.html. file not found")
    except Exception as e:
        print(f"An error has occurred: {e}")

       




local_button = tk.Button(text="Click here for my Local Weather Station", command=show_local_weather)
local_button.pack(pady=10)

state_button = tk.Button(text="Click here for State Weather", command=prompt_for_city)
state_button.pack(pady=10)

ip_alert_button = tk.Button(text="Click here for Local IP Alerts", command=show_ip_alerts)
ip_alert_button.pack(pady=10)

state_alert_button = tk.Button(text="Click here for State Alerts", command=prompt_for_state)
state_alert_button.pack(pady=10)

quit_button = tk.Button(text="Quit", command=window.quit)
quit_button.pack(pady=10)

window.mainloop()