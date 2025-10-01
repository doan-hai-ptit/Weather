from etl.extract import fetch_weather
from etl.transform import normalize_weather_data
from etl.load import save_to_db

def run_pipeline(city):
    """
    Chạy ETL pipeline cho city: Extract → Transform → Load
    """
    print(f"▶️ Đang xử lý dữ liệu thời tiết cho {city}...")
    raw_data = fetch_weather(city)
    record = normalize_weather_data(raw_data)
    save_to_db(city, record)

