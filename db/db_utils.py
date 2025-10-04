import pandas as pd
from db.connection import get_engine
from sqlalchemy import text

def get_all_weather_by_city(city_name: str,limit=20):
    engine = get_engine()
    query = f"""
        SELECT c.city_name, f.temperature, f.feels_like, 
               f.humidity, f.wind_speed, f.weather_desc, f.dt
        FROM fact_weather f
        JOIN dim_city c ON f.city_id = c.city_id
        WHERE LOWER(c.city_name) = LOWER('{city_name}')
        ORDER BY f.dt ASC;
    """
    return pd.read_sql(query, engine)

def get_weather_by_city(city_name: str, limit=20):
    engine = get_engine()
    query = f"""
        SELECT c.city_name, f.temperature, f.feels_like, 
               f.humidity, f.wind_speed, f.weather_desc, f.dt
        FROM fact_weather f
        JOIN dim_city c ON f.city_id = c.city_id
        WHERE LOWER(c.city_name) = LOWER('{city_name}')
        ORDER BY f.dt DESC
        LIMIT {limit};
    """
    return pd.read_sql(query, engine)

def get_all_city():
    engine = get_engine()
    query = f"""
        SELECT city_name
        FROM dim_city
        ORDER BY city_name ASC;
    """
    return pd.read_sql(query, engine)

def get_forecast_by_city(city_name: str):
    engine = get_engine()
    query = text("""
        SELECT c.city_name, f.temperature, f.feels_like,
               f.humidity, f.wind_speed, f.weather_desc, f.dt
        FROM fact_weather_forecast_hourly f
        JOIN dim_city c ON f.city_id = c.city_id
        WHERE LOWER(c.city_name) = LOWER(:city_name)
          AND f.dt::date = CURRENT_DATE + INTERVAL '1 day'
        ORDER BY f.dt ASC
    """)
    return pd.read_sql(query, engine, params={"city_name": city_name})

def export_to_csv():
    engine = get_engine()
    tables = ["fact_weather", "dim_city", "raw_weather", "fact_weather_forecast_hourly"]
    for t in tables:
        df = pd.read_sql(f"SELECT * FROM {t}", engine)
        df.to_csv(f"{t}.csv", index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    export_to_csv()