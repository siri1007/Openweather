import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

export const fetchWeatherByCity = async (city) => {
  const res = await axios.get(`${BASE_URL}/weather`, { params: { city } });
  return res.data;
};

export const fetchWeatherByCoords = async (lat, lon) => {
  const res = await axios.get(`${BASE_URL}/weather/coords`, { params: { lat, lon } });
  return res.data;
};

export const fetchWeatherAuto = async () => {
  const res = await axios.get(`${BASE_URL}/weather/auto`);
  return res.data;
};
