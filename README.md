# 🌦 Weather Email Notifier

**A simple Python project that fetches real-time weather data using the Open-Meteo API.**  
It provides the current weather and a 5-hour forecast based on the given latitude and longitude.  
The project is designed to automate weather updates and send emails suggesting actions based on the weather (like carrying an umbrella if it rains).  
Using crontab, the bot can automatically send these emails every day at 7:00 am.




## Libraries and Tools Used
- **requests** – to make API calls and fetch weather data  
- **python-dotenv** – to manage environment variables securely  
- **smtplib** – to send weather updates via email  
- **schedule** – to automate and schedule weather updates within Python  
- **json** – to format and handle API responses  
- **Groq** – to analyze weather data and generate AI-powered human-readable advice  
- **crontab** – to run the bot automatically on a daily schedule 
