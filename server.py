# Name: Terry Wayne Smith
# Date: 05-07-2025
# Class: ITSE-1411-V01-Beginning Web Page Programming

from flask import Flask, Response, render_template, request
import cv2
import threading
import time
import GetUserWeather
import TerLocalWeather
import IPaddressAlertsAPI
import WeatherAlertsStateAPI
import requests


app = Flask(__name__)
camera = cv2.VideoCapture("rtsp://putpasswordhere/Preview_01_main") # leave at 0 for default webcam

frame_lock = threading.Lock()
latest_frame = None

# === Function: Continuously grab frames from the webcam in the background ===
def capture_frames():
    global latest_frame
    while True:
        success, frame= camera.read()
        if not success:
            continue
        ret, buffer = cv2.imencode('.jpg', frame)
        if ret:
            with frame_lock:
                latest_frame = buffer.tobytes()

# === Function: Snapshot update every 5 mins
def snapshot_updater():
    while True:
        time.sleep(300) # 5 mins(300 seconds)
        with frame_lock:
            if latest_frame:
                with open("static/wildflowersnapshot.jpg", "wb") as f:
                    f.write(latest_frame)
            



# === Start the background thread so it doesn't block the main app ===
threading.Thread(target=capture_frames, daemon=True).start()

# == Start snapshot updater thread ===
threading.Thread(target=snapshot_updater, daemon= True).start()

# === MJPEG Stream Route ===
@app.route("/wildflower_stream")
def stream():
    def generate():
        while True:
            with frame_lock:
                if latest_frame is None:
                    continue
                frame = latest_frame
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


# === Route to serve HTML pages ===

@app.route("/")
def root():
    return app.send_static_file("html/TerryWayneSmithindex.html")

@app.route("/TerryWayneSmithindex.html")
def serve_home():
    return app.send_static_file('html/TerryWayneSmithindex.html')

@app.route("/lone_star_weather", methods=["GET", "POST"])
def lone_star_weather():
    city_name = None
    weather_data = None
    error_message = None

    if request.method == "POST":
        city_name = request.form.get("city")
        if city_name:
            print(f"Fetching weather for city: {city_name}")
            try:
                weather_data =GetUserWeather.get_weather(city_name)
                print(f"Weather data recieved: {weather_data}")
                if not weather_data or not weather_data.get("temperature"):
                    raise ValueError("Weather data incomplete or invalid")
            except Exception as e:
                print(f"Error fetching weather for {city_name}: {e}")
                error_message = f"Could not retrieve weather data for {city_name}. It might be misspelled or not available."
                weather_data = None
        else:
            error_message = "Please enter a city name."

    return render_template("user_weather.html",
                           city_name=city_name,
                           weather_data=weather_data,
                           error_message=error_message)


@app.route("/live_local_weather.html")
def serve_live_local_weather():
    TerLocalWeather.local_weather() # Calls TerLocalWeather function
    time.sleep(0.5)
    return app.send_static_file("html/live_local_weather.html")

@app.route("/ip_alerts")
def ip_alerts_page():
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    print(f"Fetching IP alerts for visitor IP: {visitor_ip}")
    alert_info = IPaddressAlertsAPI.fetch_ip_alerts(visitor_ip)
    return render_template("local_alerts.html", data=alert_info)

@app.route("/state_alerts", methods=["GET", "POST"])
def state_alerts_page():
    state_input = None
    alert_info = None
    form_error = None

    if request.method == "POST":
        state_input = request.form.get("state")
        if state_input:
            state_input = state_input.strip().upper()
            if len(state_input) == 2:
                print(f"Fetching state alerts for: {state_input}")
                # Assumes WeatherAlertsStateAPI.fetch_state_alerts now returns data
                alert_info = WeatherAlertsStateAPI.fetch_state_alerts(state_input)
            else:
                form_error = "Please enter a valid 2-letter state abbreviation."
        else:
            form_error = "Please enter a state abbreviation."

    # Assumes state_alerts.html is now in the templates folder
    return render_template("state_alerts.html",
                           state_input=state_input,
                           data=alert_info,
                           form_error=form_error)

@app.route("/trivia.html")
def serve_trivia():
    return app.send_static_file("html/trivia.html")

@app.route("/contact.html")
def serve_contact():
    return app.send_static_file("html/contact.html")


@app.route("/multimedia.html")
def serve_multimedia():
    return app.send_static_file("html/multimedia.html")

# === run Flask App directly (For Testing Only) ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=13805)
