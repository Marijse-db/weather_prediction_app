# Weather Prediction App 🌤️

A Databricks App that predicts weather conditions 5 minutes from now using AI.

## Features
- 🌡️ Real-time weather data via Open-Meteo API
- 🤖 AI predictions using Databricks Foundation Model API (Claude Sonnet 4.5)
- 📍 Geolocation support
- 🎨 Beautiful responsive UI with dynamic backgrounds
- ⚡ Auto-refresh every 2 minutes

## Quick Start

### Local Development
```bash
# Backend
export DATABRICKS_PROFILE=your-profile
uvicorn app:app --reload --port 8000

# Frontend (new terminal)
cd frontend && npm install && npm run dev
```

Visit http://localhost:5173

### Deploy to Databricks
```bash
# Build frontend
cd frontend && npm run build && cd ..

# Create app
databricks apps create weather-prediction-app -p your-profile

# Deploy
databricks sync . /Users/you@company.com/weather-prediction-app --exclude node_modules --exclude .venv -p your-profile
databricks apps deploy weather-prediction-app --source-code-path /Workspace/Users/you@company.com/weather-prediction-app -p your-profile
```

Add Foundation Model resource via UI, then redeploy.

## Tech Stack
- Backend: FastAPI + Python
- AI: Databricks Foundation Model API
- Weather: Open-Meteo (free, no key needed)
- Frontend: React + TypeScript + Tailwind CSS
