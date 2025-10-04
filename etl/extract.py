import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
API_KEY = os.getenv("WEATHER_API")

def fetch_weather(city, lang="vi", units="metric"):
    """
    Gọi API OpenWeather để lấy dữ liệu thời tiết hiện tại của city.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}&lang={lang}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

from datetime import datetime, timedelta, timezone

def fetch_forecast(city, lang="vi", units="metric"):
    """
    Gọi API OpenWeather để lấy dự báo 5 ngày (cách nhau 3h).
    Trả về JSON gốc gồm thông tin thành phố và danh sách bản ghi,
    trong đó list đã được lọc chỉ giữ lại các bản ghi thuộc ngày mai (theo giờ VN).
    """
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units={units}&lang={lang}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    VN_TZ = timezone(timedelta(hours=7))
    tomorrow = (datetime.now(VN_TZ) + timedelta(days=1)).date()

    # Lọc các bản ghi thuộc ngày mai
    forecasts = [
        item for item in data["list"]
        if datetime.fromtimestamp(item["dt"], tz=VN_TZ).date() == tomorrow
    ]

    # ✅ Gán lại list đã lọc vào data để giữ nguyên cấu trúc JSON
    data["list"] = forecasts
    return data

if __name__ == "__main__":
    city = "Hanoi"
    print("🌤 Thời tiết hiện tại:")
    print("\n📅 Dự báo ngày mai:")
    for f in fetch_forecast(city):
        dt_txt = datetime.fromtimestamp(f["dt"]).strftime("%Y-%m-%d %H:%M")
        print(f"{dt_txt}: {f['main']['temp']}°C, {f['weather'][0]['description']}")
