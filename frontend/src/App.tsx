import { useState, useEffect } from 'react'
import { Cloud, Droplets, Wind, Thermometer, Loader2, MapPin, Clock } from 'lucide-react'
import './App.css'

interface WeatherData {
  current: {
    temperature_2m: number
    apparent_temperature: number
    relative_humidity_2m: number
    wind_speed_10m: number
    wind_direction_10m: number
    cloud_cover: number
    precipitation: number
    weather_code: number
    description: string
  }
  prediction: string
  location: {
    latitude: number
    longitude: number
    timezone: string
  }
  timestamp: string
}

function App() {
  const [weather, setWeather] = useState<WeatherData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [location, setLocation] = useState({ lat: 40.7128, lon: -74.0060 })
  const [locationName, setLocationName] = useState("New York City")

  const fetchWeather = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`/api/weather?lat=${location.lat}&lon=${location.lon}`)
      if (!response.ok) {
        throw new Error('Failed to fetch weather data')
      }
      const data = await response.json()
      setWeather(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchWeather()
    // Auto-refresh every 2 minutes
    const interval = setInterval(fetchWeather, 120000)
    return () => clearInterval(interval)
  }, [location])

  const useCurrentLocation = () => {
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            lat: position.coords.latitude,
            lon: position.coords.longitude
          })
          setLocationName("Your Location")
        },
        (error) => {
          setError('Could not get your location')
        }
      )
    }
  }

  if (loading && !weather) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-400 via-blue-500 to-blue-600 flex items-center justify-center">
        <div className="text-center text-white">
          <Loader2 className="w-16 h-16 animate-spin mx-auto mb-4" />
          <p className="text-xl">Loading weather data...</p>
        </div>
      </div>
    )
  }

  if (error && !weather) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-400 to-red-600 flex items-center justify-center">
        <div className="text-center text-white p-8">
          <h2 className="text-2xl font-bold mb-4">Error</h2>
          <p className="mb-4">{error}</p>
          <button
            onClick={fetchWeather}
            className="bg-white text-red-600 px-6 py-2 rounded-lg font-semibold hover:bg-gray-100 transition"
          >
            Try Again
          </button>
        </div>
      </div>
    )
  }

  const getBackgroundGradient = (weatherCode: number) => {
    if (weatherCode === 0 || weatherCode === 1) return 'from-blue-400 via-blue-500 to-blue-600' // Clear
    if (weatherCode === 2 || weatherCode === 3) return 'from-gray-400 via-gray-500 to-gray-600' // Cloudy
    if (weatherCode >= 61 && weatherCode <= 65) return 'from-gray-600 via-gray-700 to-gray-800' // Rain
    if (weatherCode >= 71 && weatherCode <= 77) return 'from-blue-200 via-blue-300 to-blue-400' // Snow
    if (weatherCode >= 95) return 'from-purple-600 via-purple-700 to-purple-800' // Thunderstorm
    return 'from-blue-400 via-blue-500 to-blue-600' // Default
  }

  return (
    <div className={`min-h-screen bg-gradient-to-br ${weather ? getBackgroundGradient(weather.current.weather_code) : 'from-blue-400 to-blue-600'} p-4 md:p-8`}>
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center text-white mb-8">
          <h1 className="text-4xl md:text-5xl font-bold mb-2">Weather Prediction</h1>
          <p className="text-lg opacity-90">5-Minute Forecast powered by AI</p>
        </div>

        {/* Location */}
        <div className="flex justify-center items-center gap-4 mb-6">
          <div className="flex items-center gap-2 text-white">
            <MapPin className="w-5 h-5" />
            <span className="font-semibold">{locationName}</span>
          </div>
          <button
            onClick={useCurrentLocation}
            className="bg-white/20 hover:bg-white/30 text-white px-4 py-2 rounded-lg transition backdrop-blur-sm"
          >
            Use My Location
          </button>
          <button
            onClick={fetchWeather}
            disabled={loading}
            className="bg-white/20 hover:bg-white/30 text-white px-4 py-2 rounded-lg transition backdrop-blur-sm disabled:opacity-50"
          >
            {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Refresh'}
          </button>
        </div>

        {weather && (
          <>
            {/* Current Weather Card */}
            <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 mb-6 shadow-2xl border border-white/20">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                  <Clock className="w-6 h-6" />
                  Current Weather
                </h2>
                <span className="text-white/80 text-sm">
                  {new Date(weather.timestamp).toLocaleTimeString()}
                </span>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                {/* Temperature */}
                <div className="text-center">
                  <Thermometer className="w-12 h-12 mx-auto mb-2 text-white" />
                  <div className="text-4xl font-bold text-white mb-1">
                    {Math.round(weather.current.temperature_2m)}°F
                  </div>
                  <div className="text-white/80 text-sm">
                    Feels like {Math.round(weather.current.apparent_temperature)}°F
                  </div>
                </div>

                {/* Humidity */}
                <div className="text-center">
                  <Droplets className="w-12 h-12 mx-auto mb-2 text-white" />
                  <div className="text-4xl font-bold text-white mb-1">
                    {weather.current.relative_humidity_2m}%
                  </div>
                  <div className="text-white/80 text-sm">Humidity</div>
                </div>

                {/* Wind */}
                <div className="text-center">
                  <Wind className="w-12 h-12 mx-auto mb-2 text-white" />
                  <div className="text-4xl font-bold text-white mb-1">
                    {Math.round(weather.current.wind_speed_10m)}
                  </div>
                  <div className="text-white/80 text-sm">mph</div>
                </div>

                {/* Cloud Cover */}
                <div className="text-center">
                  <Cloud className="w-12 h-12 mx-auto mb-2 text-white" />
                  <div className="text-4xl font-bold text-white mb-1">
                    {weather.current.cloud_cover}%
                  </div>
                  <div className="text-white/80 text-sm">Cloud Cover</div>
                </div>
              </div>

              <div className="mt-6 text-center">
                <div className="text-2xl font-semibold text-white">
                  {weather.current.description}
                </div>
              </div>
            </div>

            {/* 5-Minute Prediction Card */}
            <div className="bg-gradient-to-br from-white/20 to-white/10 backdrop-blur-lg rounded-3xl p-8 shadow-2xl border border-white/20">
              <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                <Cloud className="w-6 h-6" />
                5-Minute Prediction
              </h2>
              <div className="text-white/90 text-lg leading-relaxed">
                {weather.prediction}
              </div>
            </div>

            {/* Footer */}
            <div className="text-center text-white/60 text-sm mt-8">
              <p>Powered by Databricks Foundation Model API & Open-Meteo</p>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default App
