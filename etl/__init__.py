from etl.extract import fetch_weather, fetch_forecast
from etl.transform import normalize_weather_data, normalize_forecast_data
from etl.load import save_to_db, save_forecast_to_db

def run_pipeline(city):
    """
    Chạy ETL pipeline cho city: Extract → Transform → Load
    """
    print(f"▶️ Đang xử lý dữ liệu thời tiết cho {city}...")
    raw_data = fetch_weather(city)
    record = normalize_weather_data(raw_data)
    save_to_db(city, record)

def run_forecast_pipeline(city):
    data = fetch_forecast(city)  # trả về JSON gốc từ API
    city_info = data["city"]
    forecast_list = data["list"]

    for item in forecast_list:
        record = normalize_forecast_data(item, city_info)
        save_forecast_to_db(record)