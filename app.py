"""Weather Prediction Databricks App - Main FastAPI application."""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from server.weather import get_current_weather, get_weather_description
from server.llm import predict_weather

app = FastAPI(
    title="Weather Prediction App",
    description="Predict weather 5 minutes from now using AI",
    version="1.0.0"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LocationRequest(BaseModel):
    latitude: float
    longitude: float

class WeatherResponse(BaseModel):
    current: dict
    prediction: str
    location: dict
    timestamp: str

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "app": "Weather Prediction"}

@app.get("/api/weather")
async def get_weather(lat: float = 40.7128, lon: float = -74.0060):
    """
    Get current weather and 5-minute prediction.

    Args:
        lat: Latitude (default: NYC)
        lon: Longitude (default: NYC)
    """
    try:
        # Get current weather
        weather_data = await get_current_weather(latitude=lat, longitude=lon)
        current = weather_data["current"]

        # Add weather description
        weather_code = current.get("weather_code", 0)
        current["description"] = get_weather_description(weather_code)

        # Generate AI prediction
        prediction = await predict_weather(current)

        return {
            "current": current,
            "prediction": prediction,
            "location": weather_data["location"],
            "timestamp": weather_data["timestamp"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/weather")
async def get_weather_for_location(location: LocationRequest):
    """Get weather for a specific location."""
    return await get_weather(lat=location.latitude, lon=location.longitude)

# Serve React frontend (when built)
frontend_dir = os.path.join(os.path.dirname(__file__), "frontend", "dist")
if os.path.exists(frontend_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dir, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve the React SPA for all non-API routes."""
        if not full_path.startswith("api"):
            return FileResponse(os.path.join(frontend_dir, "index.html"))
