# importing necessary libaries
from groq import Groq
from dotenv import load_dotenv
import os
import json
from fetch_weather import get_weather

load_dotenv()

# Creating Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# function to fetch data 
def generate_advice(weather_data, location=""):
    if not weather_data:
        return "Weather data not available."

    weather_text = json.dumps(weather_data, indent=2)
# prompt to generate ai advice
    prompt = (
        f"Here is the current weather data for {location}:\n"
        f"{weather_text}\n\n"
        "Provide concise weather advice including:\n"
        "1. Current temperature\n"
        "2. Rain expectation for next few hours\n"
        "3. Whether to carry an umbrella\n"
        "4. aware about any emergency like flood, heavy rainfall,strom,earthquake,snowfall or any thing else based on weather\n"
        "5. What clothes to wear\n\n"
        "6.Also give me  adive that you want me to do in that weather conditon\n\n"
        "No greetings. No signatures."
    )
# llm
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=200
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {e}"



if __name__ == "__main__":
    weather_data = get_weather()
    advice = generate_advice(weather_data, location="Kathmandu")
    print(advice)
