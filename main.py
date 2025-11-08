import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from dotenv import load_dotenv
from typing import Optional
from weather_agent import get_weather, generate_advice
from email_service import send_email

load_dotenv()

app = FastAPI(title="Weather Notifier API", version="1.0.0")


# Request Models
class WeatherRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude between -90 and 90")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude between -180 and 180")


class WeatherAdviceRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude between -90 and 90")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude between -180 and 180")
    location: str = Field(..., min_length=1, description="Location name")


class SendEmailRequest(BaseModel):
    subject: str = Field(..., min_length=1, description="Email subject")
    body: str = Field(..., min_length=1, description="Email body content")
    to_email: EmailStr = Field(..., description="Recipient email address")


# Response Models
class WeatherResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    message: Optional[str] = None


class WeatherAdviceResponse(BaseModel):
    success: bool
    advice: Optional[str] = None
    location: Optional[str] = None
    message: Optional[str] = None


class EmailResponse(BaseModel):
    success: bool
    message: str


@app.get("/")
async def root():
    return {
        "message": "Weather Notifier API",
        "endpoints": {
            "/weather": "GET weather details (requires latitude and longitude)",
            "/weather/advice": "POST AI weather advice (requires latitude, longitude, and location)",
            "/send-email": "POST send email (requires subject, body, and to_email)"
        }
    }


@app.post("/weather", response_model=WeatherResponse)
async def get_weather_details(request: WeatherRequest):
    """
    Get weather details for given latitude and longitude.
    Returns current weather and next 5-hour forecast.
    """
    try:
        weather_data = get_weather(request.latitude, request.longitude)
        
        if not weather_data:
            raise HTTPException(status_code=404, detail="Weather data not available")
        
        return WeatherResponse(
            success=True,
            data=weather_data,
            message="Weather data retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weather: {str(e)}")


@app.post("/weather/advice", response_model=WeatherAdviceResponse)
async def get_weather_advice(request: WeatherAdviceRequest):
    """
    Get AI-powered weather advice for given location.
    Returns personalized advice including temperature, forecast, and clothing suggestions.
    """
    try:
        weather_data = get_weather(request.latitude, request.longitude)
        
        if not weather_data:
            raise HTTPException(status_code=404, detail="Weather data not available")
        
        advice = generate_advice(weather_data, location=request.location)
        
        if not advice or advice == "Failed to generate AI advice.":
            raise HTTPException(status_code=500, detail="Failed to generate AI advice")
        
        return WeatherAdviceResponse(
            success=True,
            advice=advice,
            location=request.location,
            message="Weather advice generated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating advice: {str(e)}")


@app.post("/send-email", response_model=EmailResponse)
async def send_email_endpoint(request: SendEmailRequest):
    """
    Send an email with the provided subject, body, and recipient.
    """
    try:
        send_email(request.subject, request.body, request.to_email)
        return EmailResponse(
            success=True,
            message=f"Email sent successfully to {request.to_email}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
