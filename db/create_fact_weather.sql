CREATE TABLE fact_weather (
    id SERIAL PRIMARY KEY,
    city_id INT,
    dt TIMESTAMP,            -- thời điểm đo
    temperature FLOAT,
    feels_like FLOAT,
    humidity INT,
    weather_desc VARCHAR(255),
    wind_speed FLOAT,
    visibility INT,
	updated_at TIMESTAMP DEFAULT NOW()
);