import os
from dotenv import load_dotenv
from weather_agent import get_weather, generate_advice
from email_service import send_email

load_dotenv()

LATITUDE = float(os.getenv("LATITUDE", 27.7172))
LONGITUDE = float(os.getenv("LONGITUDE", 85.3240))
LOCATION = os.getenv("LOCATION", "Kathmandu")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

if __name__ == "__main__":
  
    weather = get_weather(LATITUDE, LONGITUDE)


    advice = generate_advice(weather, location=LOCATION) if weather else "Weather data not available."


    email_body = f"Weather advice for {LOCATION}:\n\n{advice}"

    send_email("AI Weather Suggestion", email_body, RECIPIENT_EMAIL)
