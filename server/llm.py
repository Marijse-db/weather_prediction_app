"""Foundation Model API integration."""
import os
from openai import AsyncOpenAI
from .config import get_oauth_token, get_workspace_host, IS_DATABRICKS_APP

def get_llm_client() -> AsyncOpenAI:
    """Get OpenAI-compatible client for Databricks Foundation Models."""
    host = get_workspace_host()

    if IS_DATABRICKS_APP:
        # Remote: Use service principal token
        token = os.environ.get("DATABRICKS_TOKEN") or get_oauth_token()
    else:
        # Local: Use profile token
        token = get_oauth_token()

    return AsyncOpenAI(
        api_key=token,
        base_url=f"{host}/serving-endpoints"
    )

async def predict_weather(current_conditions: dict) -> str:
    """Use Foundation Model to predict weather 5 minutes from now."""
    client = get_llm_client()
    model = os.environ.get("SERVING_ENDPOINT", "databricks-claude-sonnet-4-5")

    # Build prompt with current conditions
    prompt = f"""You are a weather prediction AI. Based on the current weather conditions below, predict what the weather will be like in 5 minutes from now.

Current Conditions:
- Temperature: {current_conditions.get('temperature_2m')}°F
- Feels Like: {current_conditions.get('apparent_temperature')}°F
- Humidity: {current_conditions.get('relative_humidity_2m')}%
- Wind Speed: {current_conditions.get('wind_speed_10m')} mph
- Wind Direction: {current_conditions.get('wind_direction_10m')}°
- Cloud Cover: {current_conditions.get('cloud_cover')}%
- Precipitation: {current_conditions.get('precipitation')} mm
- Weather Code: {current_conditions.get('weather_code')}

Provide a brief, conversational prediction (2-3 sentences) about what the weather will be like in exactly 5 minutes. Be realistic - in 5 minutes, weather typically doesn't change dramatically unless there's an active weather event. Include any relevant advice or observations."""

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a meteorologist making very short-term weather predictions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating prediction: {str(e)}"
