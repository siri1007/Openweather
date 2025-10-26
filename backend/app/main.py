from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from cachetools import TTLCache
from dotenv import load_dotenv
from datetime import datetime
from collections import defaultdict
import requests
import os


from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker


load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")


DATABASE_URL = "sqlite:///./weather_preferences.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class UserPreferences(Base):
    __tablename__ = "preferences"
    id = Column(Integer, primary_key=True, index=True)
    default_city = Column(String, default="Hyderabad")
    units = Column(String, default="metric")
    language = Column(String, default="en")

Base.metadata.create_all(bind=engine)


def get_user_preferences():
    db = SessionLocal()
    prefs = db.query(UserPreferences).first()
    if not prefs:
        prefs = UserPreferences()
        db.add(prefs)
        db.commit()
        db.refresh(prefs)
    db.close()
    return prefs


app = FastAPI(title="Weather API Proxy", version="4.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


weather_cache = TTLCache(maxsize=100, ttl=600) 
ip_cache = TTLCache(maxsize=100, ttl=600)       


def extract_weather(data, forecast_data):
    city_name = data["name"]
    temperature = round(data["main"]["temp"], 1)
    description = data["weather"][0]["description"].title()
    icon = data["weather"][0]["icon"]

    timezone_offset = data["timezone"]
    local_time = datetime.utcfromtimestamp(data["dt"] + timezone_offset)
    time_str = local_time.strftime("%H:%M")
    date_str = local_time.strftime("%d %b %Y")

    forecast_by_day = defaultdict(list)
    for item in forecast_data["list"]:
        local_dt = datetime.utcfromtimestamp(item["dt"] + timezone_offset)
        day = local_dt.strftime("%a, %d %b")
        temp = round(item["main"]["temp"], 1)
        desc = item["weather"][0]["description"].title()
        icon = item["weather"][0]["icon"]
        forecast_by_day[day].append({
            "time": local_dt.strftime("%H:%M"),
            "temp": temp,
            "description": desc,
            "icon": icon
        })

    forecast = [{"date": day, "data": data} for day, data in forecast_by_day.items()]

    return {
        "city": city_name,
        "temperature": temperature,
        "description": description,
        "icon": icon,
        "forecast": forecast,
        "local_time": time_str,
        "local_date": date_str
    }


@app.get("/weather")
@limiter.limit("10/minute")
async def get_weather(request: Request, city: str):
    cache_key = f"weather_{city.lower()}"
    if cache_key in weather_cache:
        return weather_cache[cache_key]

    try:
        prefs = get_user_preferences()
        params = {
            "q": city,
            "appid": API_KEY,
            "units": prefs.units,
            "lang": prefs.language
        }
        current = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)
        forecast = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=params)
        current.raise_for_status()
        forecast.raise_for_status()

        result = extract_weather(current.json(), forecast.json())
        weather_cache[cache_key] = result
        return result
    except:
        raise HTTPException(status_code=404, detail="City not found")


@app.get("/weather/coords")
@limiter.limit("10/minute")
async def get_weather_by_coords(request: Request, lat: float, lon: float):
    cache_key = f"weather_{lat}_{lon}"
    if cache_key in weather_cache:
        return weather_cache[cache_key]

    try:
        prefs = get_user_preferences()
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": prefs.units,
            "lang": prefs.language
        }
        current = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)
        forecast = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=params)
        current.raise_for_status()
        forecast.raise_for_status()

        result = extract_weather(current.json(), forecast.json())
        weather_cache[cache_key] = result
        return result
    except:
        raise HTTPException(status_code=404, detail="Location not found")


@app.get("/weather/auto")
@limiter.limit("5/minute")
async def get_weather_auto(request: Request):
    ip = request.client.host

    if ip in ip_cache:
        lat, lon = ip_cache[ip]
    else:
        try:
            res = requests.get(f"http://ip-api.com/json/{ip}")
            data = res.json()
            lat, lon = data.get("lat"), data.get("lon")
            ip_cache[ip] = (lat, lon)
        except:
            raise HTTPException(status_code=400, detail="Unable to detect location")

    return await get_weather_by_coords(request, lat=lat, lon=lon)


@app.get("/geolocate")
async def geolocate(request: Request):
    ip = request.client.host
    if ip in ip_cache:
        lat, lon = ip_cache[ip]
    else:
        try:
            res = requests.get(f"http://ip-api.com/json/{ip}")
            data = res.json()
            lat, lon = data.get("lat"), data.get("lon")
            ip_cache[ip] = (lat, lon)
        except:
            raise HTTPException(status_code=400, detail="Unable to detect location")

    return {"ip": ip, "lat": lat, "lon": lon}


@app.get("/preferences")
def read_preferences():
    prefs = get_user_preferences()
    return {
        "default_city": prefs.default_city,
        "units": prefs.units,
        "language": prefs.language
    }

@app.post("/preferences")
def update_preferences(default_city: str = None, units: str = None, language: str = None):
    db = SessionLocal()
    prefs = db.query(UserPreferences).first()
    if not prefs:
        prefs = UserPreferences()
        db.add(prefs)

    if default_city:
        prefs.default_city = default_city
    if units:
        prefs.units = units
    if language:
        prefs.language = language

    db.commit()
    db.refresh(prefs)
    db.close()

    return {
        "message": "Preferences updated",
        "default_city": prefs.default_city,
        "units": prefs.units,
        "language": prefs.language
    }
