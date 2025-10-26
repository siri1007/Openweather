import React from "react";

export default function WeatherCard({ weather, addFavorite }) {
  return (
    <div className="weather-card">
      <h2>{weather.city}</h2>
      <div className="main-weather">
        <img
          src={`http://openweathermap.org/img/wn/${weather.icon}@2x.png`}
          alt="weather icon"
        />
        <div className="temp-desc">
          <p className="temp">{weather.temperature}°C</p>
          <p className="desc">{weather.description}</p>
        </div>
      </div>

      <div className="weather-details">
        <div className="detail-item">
               <img src="images/Humidity.png" alt="Humidity" className="icon" />
          <span>Humidity: {weather.humidity || weather.humidity} %</span>
        </div>
        <div className="detail-item">
          <img src="images/wind.png" alt="wind" className="icon" />
          <span>Wind: {weather.wind_speed || weather.wind_speed} m/s</span>
        </div>
        <div className="detail-item">
          <img src="images/pressure.webp" alt="pressure" className="icon" />
          <span>Pressure: {weather.pressure || weather.pressure} hPa</span>
        </div>
      </div>

      <button className="fav-btn" onClick={() => addFavorite(weather.city)}>
        Add to Favorites
      </button>
    </div>
  );
}
