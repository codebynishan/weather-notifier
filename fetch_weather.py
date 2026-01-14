# importing necessary libraries
import requests
from datetime import datetime

# Fetching location using IP
def get_location():
    url = "http://ip-api.com/json/"
    response = requests.get(url)
    data = response.json()
    return data["lat"], data["lon"], data["city"], data["country"]

# Fetch weather data from Open-Meteo
def get_weather():
    lat, lon, city, country = get_location()

    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&current_weather=true"
        "&hourly=temperature_2m,relative_humidity_2m,windspeed_10m,rain"
        "&timezone=Asia/Kathmandu"
    )

    response = requests.get(url)
    data = response.json()

    current = data.get("current_weather")
    hourly = data.get("hourly")

    if not current or not hourly:
        return None, city, country

    times = hourly["time"]
    temperatures = hourly["temperature_2m"]
    humidity = hourly["relative_humidity_2m"]
    windspeed = hourly["windspeed_10m"]
    rain = hourly["rain"]

    # Get current hour index
    now = datetime.now().strftime("%Y-%m-%dT%H:00")

    try:
        current_index = times.index(now)
    except ValueError:
        current_index = 0  

    # Get next 5 hours forecast
    next_5_hours = []
    for i in range(current_index + 1, current_index + 6):
        next_5_hours.append({
            "time": times[i],
            "temperature": temperatures[i],
            "humidity": humidity[i],
            "windspeed": windspeed[i],
            "rain": rain[i]
        })

    return {
        "current": current,
        "next_5_hours": next_5_hours
    }, city, country

#  weather summary
def print_weather_summary(weather_data, city):
    current = weather_data["current"]
    forecast = weather_data["next_5_hours"]

    print(f"\nCurrent temperature in {city} is {current['temperature']}°C.\n")
    print("Next 5 hours forecast:")

    for hour in forecast:
        time = datetime.fromisoformat(hour["time"]).strftime("%I:%M %p").lstrip("0")
        rain_text = "rain" if hour["rain"] > 0 else "no rain"

        print(
            f"Time {time}: {hour['temperature']}°C, "
            f"Wind {hour['windspeed']} m/s, "
            f"Humidity {hour['humidity']}%, {rain_text}"
        )


weather_data, city, country = get_weather()

if weather_data:
    print_weather_summary(weather_data, city)
else:
    print("Weather data not available.")
