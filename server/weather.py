"""Weather data service."""
import os
import aiohttp
from typing import Dict, Any

# Free weather API - no key needed for limited requests
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

async def get_current_weather(latitude: float = 40.7128, longitude: float = -74.0060) -> Dict[str, Any]:
    """
    Fetch current weather conditions using Open-Meteo API (no API key needed).

    Default location: New York City
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,cloud_cover,wind_speed_10m,wind_direction_10m",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "timezone": "auto"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(WEATHER_API_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return {
                    "location": {
                        "latitude": latitude,
                        "longitude": longitude,
                        "timezone": data.get("timezone", "Unknown")
                    },
                    "current": data.get("current", {}),
                    "timestamp": data.get("current", {}).get("time", "")
                }
            else:
                raise Exception(f"Weather API error: {response.status}")

def get_weather_description(weather_code: int) -> str:
    """Convert WMO weather code to description."""
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return weather_codes.get(weather_code, "Unknown")
