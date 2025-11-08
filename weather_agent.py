import requests
import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_weather(lat, lon):
    """Fetch current weather and next 5-hour forecast."""
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current_weather=true"
            f"&hourly=temperature_2m,apparent_temperature,relative_humidity_2m,windspeed_10m,rain"
        )
        response = requests.get(url)
        data = response.json()

        current = data.get("current_weather", {})
        hourly = data.get("hourly", {})

        if not current:
            return None

        next_5_hours = [
            {
                "time": hourly["time"][i],
                "temperature": hourly["temperature_2m"][i],
                "apparent_temperature": hourly["apparent_temperature"][i],
                "humidity": hourly["relative_humidity_2m"][i],
                "windspeed": hourly["windspeed_10m"][i],
                "rain": hourly["rain"][i]
            }
            for i in range(1, min(6, len(hourly.get("time", []))))
        ]

        return {"current": current, "next_5_hours": next_5_hours}

    except Exception as e:
        print("Error fetching weather:", e)
        return None

def generate_advice(weather_data, location=""):
    """Generate human-readable AI advice based on weather data and location."""
    if not weather_data:
        return "Weather data not available."

    data_text = json.dumps(weather_data, indent=4)
    user_prompt = (
          f"Here is the current weather data for {location}:\n{data_text}\n\n"
        "Please provide a short, clear, human-readable advice based on this data. "
        "Include:\n"
        "1. Current temperature.\n"
        "2. Next 5 hours forecast (temperature and rain).\n"
        "3. A simple suggestion about whether to carry an umbrella or not.\n"
        "4. Suggest what kind of clothes the user should wear according to the weather conditions.\n\n"
        "Important: Do NOT include any formal greetings, signatures, 'Stay updated', 'Best regards', or your name. "
        "Only provide the relevant weather advice in a concise, email-ready format."
)

    

    try:
        llm_response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": user_prompt}],
            max_tokens=250,
            temperature=0.2
        )
        advice = llm_response.choices[0].message.content
        return advice
    except Exception as e:
        print("Error generating AI advice:", e)
        return "Failed to generate AI advice."
