from db.db_utils import get_all_city
from etl import run_forecast_pipeline
from datetime import datetime

def main():
    print("🚀 Bắt đầu thu thập dữ liệu dự báo ngày mai...")
    city_df = get_all_city()
    for city in city_df["city_name"]:
        run_forecast_pipeline(city)
    print(f"✅ Hoàn tất lúc {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()