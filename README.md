# 🌦️ Weather Dashboard

A full-stack Weather Dashboard built with FastAPI (backend) and React (frontend). It shows real-time weather, autocomplete suggestions, recent searches, and visual charts, all using data from the OpenWeatherMap API. The app is responsive, clean, and great for exploring weather data visually while practicing modern Python tools.


## 🔧 Tech Stack

### Frontend (React)
- React.js
- Recharts (📊 for visualizations)
- CSS (Custom Responsive Styling)
- OpenWeatherMap Geocoding API
- OpenWeatherMap Weather API

### Backend (FastAPI)
- FastAPI
- Requests (API integration)
- CORS Middleware
- Uvicorn

---

## 📦 Features

- 🔍 **Auto-location Weather**: Uses Geolocation API to fetch current weather on page load.
- 🏙️ **City Search**: Type any city to get live weather data.
- 🧠 **Autocomplete Suggestions**: Powered by OpenWeatherMap Geocoding API.
- 🕘 **Recent Search History**: Stored via `localStorage`, clickable for quick access.
- 📊 **Chart Dashboard**: Visual representation of weather data using Recharts.
- 📱 **Mobile Friendly**: Fully responsive UI.
- ⚙️ **.env Configurable**: Clean environment variable usage for both frontend & backend.

---

## 🌍 How to Run the Project Locally

### 📁 Clone the Repository

```bash
git clone URL
cd weather-dashboard
````



## 🖥️ Frontend Setup

```bash
cd frontend
npm install
```

### 📄 Create `.env` in `frontend/` with:

```env
REACT_APP_OPENWEATHER_API_KEY=your_openweathermap_api_key
```

### ▶️ Start Frontend

```bash
npm start
```

---

## ⚙️ Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 📄 Create `.env` in `backend/` with:

```env
OPENWEATHER_API_KEY=your_openweathermap_api_key
```

### ▶️ Start Backend

```bash
uvicorn app.main:app --reload
```

---
