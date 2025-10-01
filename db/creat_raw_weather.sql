CREATE TABLE raw_weather (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100),
    json_data JSONB,
    collected_at TIMESTAMP DEFAULT NOW()
);
