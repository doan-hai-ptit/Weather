import pandas as pd
from db.connection import get_engine

def show_fact_weather(limit=5):
    query = f"""
        SELECT f.id, c.city_name, f.temperature, f.feels_like, 
               f.humidity, f.wind_speed, f.weather_desc
        FROM fact_weather f
        JOIN dim_city c ON f.city_id = c.city_id
        ORDER BY f.dt DESC
        LIMIT {limit};
    """
    try:
        engine = get_engine()
        df = pd.read_sql(query, engine)
        print("\n📊 Kết quả dữ liệu trong fact_weather:\n")
        for _, row in df.iterrows():
            city = row["city_name"]
            temp = row["temperature"]
            feels_like = row["feels_like"]
            weather_desc = row["weather_desc"]
            humidity = row["humidity"]
            wind = row["wind_speed"]

            print(f"🌍 Thời tiết tại {city}:")
            print(f"- Nhiệt độ: {temp}°C (cảm giác như {feels_like}°C)")
            print(f"- Trạng thái: {weather_desc}")
            print(f"- Độ ẩm: {humidity}%")
            print(f"- Gió: {wind} m/s")
            print("-----")
    except Exception as e:
        print("❌ Lỗi khi lấy dữ liệu:", e)

if __name__ == "__main__":
    show_fact_weather(5)
