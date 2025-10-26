import React, { useState, useEffect } from "react";
import axios from "axios";
import SearchBar from "./components/SearchBar";
import WeatherCard from "./components/WeatherCard";
import ForecastChart from "./components/ForecastChart";
import Favorites from "./components/Favorites";
import "./styles/App.css";


const BACKEND_URL = "http://127.0.0.1:8000";

function App() {
  const [city, setCity] = useState("");
  const [weather, setWeather] = useState(null);
  const [favorites, setFavorites] = useState(
    JSON.parse(localStorage.getItem("favorites")) || []
  );

  const fetchWeather = async (cityName) => {
    try {
      const res = await axios.get(`${BACKEND_URL}/weather`, {
        params: { city: cityName },
      });
      setWeather(res.data);
      setCity(cityName);
    } catch (err) {
      alert("City not found");
    }
  };

  const addFavorite = (cityName) => {
    if (!favorites.includes(cityName)) {
      const newFavs = [...favorites, cityName];
      setFavorites(newFavs);
      localStorage.setItem("favorites", JSON.stringify(newFavs));
    }
  };

  const removeFavorite = (cityName) => {
    const newFavs = favorites.filter((c) => c !== cityName);
    setFavorites(newFavs);
    localStorage.setItem("favorites", JSON.stringify(newFavs));
  };

  useEffect(() => {

    axios.get(`${BACKEND_URL}/preferences`).then((res) => {
      fetchWeather(res.data.default_city);
    });
  }, []);

  return (
    <div className="App">
      <h1>Weather Dashboard</h1>
      <div className="dashboard">
        <SearchBar fetchWeather={fetchWeather} />
        <Favorites
          favorites={favorites}
          fetchWeather={fetchWeather}
          removeFavorite={removeFavorite}
        />
        {weather && (
          <>
            <WeatherCard weather={weather} addFavorite={addFavorite} />
            <div className="forecast-chart">
              <h3>5-Day Forecast</h3>
              <ForecastChart forecast={weather.forecast} />
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
