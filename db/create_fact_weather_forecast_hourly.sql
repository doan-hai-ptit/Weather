CREATE TABLE fact_weather_forecast_hourly (
    id SERIAL PRIMARY KEY,
    city_id INT REFERENCES dim_city(city_id),
    dt TIMESTAMP,         -- Thời điểm dự báo cụ thể (vd: 2025-10-05 03:00)
    temperature FLOAT,
    feels_like FLOAT,
    humidity INT,
    weather_desc TEXT,
    wind_speed FLOAT,
    visibility INT,
    collected_at TIMESTAMP DEFAULT NOW()
);
