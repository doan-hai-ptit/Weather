import json
from db.connection import get_connection

def save_to_db(city, record):
    """
    Lưu dữ liệu vào PostgreSQL:
    - raw_weather
    - dim_city
    - fact_weather
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        # 1. Lưu raw_weather
        cur.execute("""
            INSERT INTO raw_weather(city, json_data, collected_at)
            VALUES (%s, %s, NOW())
        """, (city, json.dumps(record["raw"], ensure_ascii=False)))

        # 2. Lưu dim_city (nếu chưa có)
        cur.execute("""
            INSERT INTO dim_city(city_name, country, latitude, longitude)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (city_name) DO NOTHING
        """, (record["city_name"], record["country"], record["lat"], record["lon"]))

        # 3. Lưu fact_weather
        cur.execute("""
            INSERT INTO fact_weather(city_id, dt, temperature, feels_like, humidity, wind_speed, weather_desc, visibility ,updated_at)
            SELECT city_id, %s, %s, %s, %s, %s, %s, %s, NOW()
            FROM dim_city WHERE city_name = %s
        """, (record["dt"], record["temp"], record["feels_like"], record["humidity"], record["wind_speed"],
             record["weather_desc"],record["visibility"] ,record["city_name"]))

        conn.commit()
        print(f"✅ Đã lưu dữ liệu thời tiết cho {city} vào database")
    except Exception as e:
        conn.rollback()
        print("❌ Lỗi khi lưu DB:", e)
    finally:
        cur.close()
        conn.close()
