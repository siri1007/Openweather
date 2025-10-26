import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

export default function ForecastChart({ forecast }) {

  const chartData = [];
  forecast.forEach((day) => {
    day.data.forEach((item) => {
      chartData.push({
        time: `${day.date} ${item.time}`,
        date: day.date,
        temp: item.temp,
      });
    });
  });


  const dayLabels = forecast.slice(0, 5).map((d) => d.date);

  const totalPoints = chartData.length;
  const tickIndexes = Array.from({ length: 5 }, (_, i) =>
    Math.floor((i * totalPoints) / 5)
  );

  return (
    <div style={{ width: "100%", height: 320 }}>
      <ResponsiveContainer>
        <LineChart
          data={chartData}
          margin={{ top: 30, right: 30, left: 10, bottom: 30 }}
        >
          <CartesianGrid strokeDasharray="3 3" opacity={0.2} />

    
          <XAxis
            dataKey="time"
            tickFormatter={(value, index) => {
              const day = value.split(" ")[0];
              return tickIndexes.includes(index) ? day : "";
            }}
            interval={0}
            tick={{ fill: "#9c33c5ff", fontSize: 13 }}
            height={60}
            angle={-20}
            textAnchor="end"
          />

          <YAxis
            tick={{ fill: "#9f68c5ff", fontSize: 13 }}
            domain={["auto", "auto"]}
            width={50}
          />

          <Tooltip
            contentStyle={{
              backgroundColor: "#222",
              borderRadius: "8px",
              color: "#fff",
            }}
            labelStyle={{ color: "#fff" }}
            formatter={(value) => [`${value}°C`, "Temperature"]}
          />

          <Line
            type="monotone"
            dataKey="temp"
            stroke="#ffcc00"
            strokeWidth={3}
            dot={false}
            activeDot={{ r: 5, fill: "#ffcc00" }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
