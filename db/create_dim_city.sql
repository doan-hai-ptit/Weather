CREATE TABLE dim_city (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) UNIQUE,
    country VARCHAR(10),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);
