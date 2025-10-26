import React from "react";

export default function Favorites({ favorites, fetchWeather, removeFavorite }) {
  return (
    <div className="favorites">
      <h3>Favorites</h3>
      {favorites.map((city) => (
        <div key={city} className="favorite-item">
          <span onClick={() => fetchWeather(city)}>{city}</span>
          <button onClick={() => removeFavorite(city)}>X</button>
        </div>
      ))}
    </div>
  );
}
