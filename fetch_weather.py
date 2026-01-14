#  importing required library for fetching weather api
import os
import requests
from dotenv import load_dotenv

# load variable from .env file
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

# fetch api location data 
def get_location():
  url="http://ip-api.com/json/"
  response=requests.get(url)
  data=response.json()
  return data["lat"], data["lon"], data["city"], data["country"]


#  fetch api weather data
def getweather():
  lon,lat,city,country=get_location()
  url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )

  response = requests.get(url)
  return response.json(), city, country

data, city, country = getweather()
print(get_location())
print(getweather())
print(f"""
Location: {city}, {country}
Weather: {data['weather'][0]['description'].title()}
Temperature: {data['main']['temp']}°C
Feels Like: {data['main']['feels_like']}°C
Humidity: {data['main']['humidity']}%
Wind Speed: {data['wind']['speed']} m/s
""")

