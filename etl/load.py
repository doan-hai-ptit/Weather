import json
from db.connection import get_connection

def save_to_db(city, record):
    """
    Lưu dữ liệu vào PostgreSQL:
    - raw_weather (1 bản ghi / ngày / city)
    - dim_city
    - fact_weather (1 bản ghi / ngày / city)
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        # 1. Lưu raw_weather (1 bản ghi / city / ngày)
        cur.execute("""
            INSERT INTO raw_weather(city, json_data, collected_at)
            SELECT %s, %s, NOW()
            WHERE NOT EXISTS (
                SELECT 1 FROM raw_weather 
                WHERE city = %s AND DATE(collected_at) = CURRENT_DATE
            )
        """, (city, json.dumps(record["raw"], ensure_ascii=False), city))

        # 2. Lưu dim_city (nếu chưa có)
        cur.execute("""
            INSERT INTO dim_city(city_name, country, latitude, longitude)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (city_name) DO NOTHING
        """, (record["city_name"], record["country"], record["lat"], record["lon"]))

        # 3. Lưu fact_weather (1 bản ghi / city / ngày)
        cur.execute("""
            INSERT INTO fact_weather(city_id, dt, temperature, feels_like, humidity, wind_speed, weather_desc, visibility, updated_at)
            SELECT city_id, %s, %s, %s, %s, %s, %s, %s, NOW()
            FROM dim_city 
            WHERE city_name = %s
              AND NOT EXISTS (
                  SELECT 1 FROM fact_weather f
                  JOIN dim_city c ON f.city_id = c.city_id
                  WHERE c.city_name = %s AND DATE(f.dt) = DATE(%s)
              )
        """, (record["dt"], record["temp"], record["feels_like"], record["humidity"], record["wind_speed"],
              record["weather_desc"], record["visibility"], record["city_name"],
              record["city_name"], record["dt"]))

        conn.commit()
        print(f"✅ Đã lưu dữ liệu thời tiết cho {city} vào database")
    except Exception as e:
        conn.rollback()
        print("❌ Lỗi khi lưu DB:", e)
    finally:
        cur.close()
        conn.close()
        
def save_forecast_to_db(record):
    conn = get_connection()
    cur = conn.cursor()
    try:
        forecast_for = record["dt"].date()  # ngày dự báo (từ timestamp)

        cur.execute("""
            INSERT INTO fact_weather_forecast_hourly
            (city_id, dt, temperature, feels_like, humidity, wind_speed, weather_desc, visibility, collected_at)
            SELECT city_id, %s, %s, %s, %s, %s, %s, %s, NOW()
            FROM dim_city
            WHERE city_name = %s
        """, (
            record["dt"],            # dt
            record["temp"],          # temperature
            record["feels_like"],    # feels_like
            record["humidity"],      # humidity
            record["wind_speed"],    # wind_speed
            record["weather_desc"],  # weather_desc
            record["visibility"],    # visibility
            record["city_name"]      # city_name (WHERE)
        ))

        conn.commit()
        print(f"✅ Đã lưu dự báo thời tiết theo giờ cho {record['city_name']} lúc {record['dt']}")
    except Exception as e:
        conn.rollback()
        print("❌ Lỗi khi lưu DB:", e)
    finally:
        cur.close()
        conn.close()
