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

**Important:** The `.databricksignore` file automatically excludes `node_modules` and other unnecessary files from deployment.

```bash
# 1. Build frontend in Databricks notebook (upload build_frontend.py)
# Run build_frontend.py notebook in your Databricks workspace

# 2. Create app
databricks apps create weather-prediction-app -p your-profile

# 3. Sync code to workspace (excludes node_modules via .databricksignore)
databricks workspace import-dir . /Workspace/Users/you@company.com/weather-prediction-app -p your-profile

# 4. Deploy
databricks apps deploy weather-prediction-app --source-code-path /Workspace/Users/you@company.com/weather-prediction-app -p your-profile
```

**Note:** The app.yaml includes Foundation Model resource configuration. No manual resource addition needed!

## Tech Stack
- Backend: FastAPI + Python
- AI: Databricks Foundation Model API
- Weather: Open-Meteo (free, no key needed)
- Frontend: React + TypeScript + Tailwind CSS
