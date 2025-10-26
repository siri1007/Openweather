import React, { useState } from "react";

export default function SearchBar({ fetchWeather }) {
  const [input, setInput] = useState("");

  const handleSearch = () => {
    if (input.trim() !== "") {
      fetchWeather(input.trim());
      setInput("");
    }
  };

  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Search city..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSearch()}
      />
      <button onClick={handleSearch}>Search</button>
    </div>
  );
}
