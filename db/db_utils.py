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
        ORDER BY f.dt ASC
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
          AND (f.dt AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Ho_Chi_Minh')::date = CURRENT_DATE + INTERVAL '1 day'
        ORDER BY f.dt ASC
    """)
    return pd.read_sql(query, engine, params={"city_name": city_name})

def get_forecast_today_by_city(city_name: str):
    engine = get_engine()
    query = text("""
        SELECT c.city_name, f.temperature, f.feels_like,
               f.humidity, f.wind_speed, f.weather_desc, f.dt
        FROM fact_weather_forecast_hourly f
        JOIN dim_city c ON f.city_id = c.city_id
        WHERE LOWER(c.city_name) = LOWER(:city_name)
          AND (f.dt AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Ho_Chi_Minh')::date = CURRENT_DATE
        ORDER BY f.dt ASC
    """)
    return pd.read_sql(query, engine, params={"city_name": city_name})

def export_to_csv():
    engine = get_engine()
    tables = ["fact_weather", "dim_city", "raw_weather", "fact_weather_forecast_hourly"]

    for t in tables:
        df = pd.read_sql(f"SELECT * FROM {t}", engine)

        for col in df.columns:
            col_lower = col.lower()

            # 1️⃣ Chuẩn hóa các cột id / city_id về int
            if "id" in col_lower:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

            # 2️⃣ Chuẩn hóa cột thời gian dt
            elif "dt" in col_lower:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

                def normalize_timestamp(x):
                    # Nếu nhỏ hơn 10^11 (ví dụ 1759626000) → đã đúng (tính theo giây)
                    if x < 1e11:
                        return int(x)
                    # Nếu có 13 chữ số (mili giây) → chia 1000
                    elif x < 1e15:
                        return int(x / 1000)
                    # Nếu có 16–19 chữ số (micro/nano giây) → chia 1_000_000_000
                    else:
                        return int(x / 1_000_000_000)

                df[col] = df[col].apply(normalize_timestamp)

        # Xuất ra CSV
        df.to_csv(f"{t}.csv", index=False, encoding="utf-8-sig")

        print(f"✅ Đã export bảng {t} (đã chuẩn hóa kiểu dữ liệu).")

    print("🎉 Đã xuất toàn bộ bảng ra CSV thành công, an toàn để import vào Supabase.")
if __name__ == "__main__":
    export_to_csv()