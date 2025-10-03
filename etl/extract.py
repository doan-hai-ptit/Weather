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
    Trả về list các bản ghi thuộc ngày mai.
    """
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units={units}&lang={lang}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Lấy ngày mai theo UTC có timezone-aware
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()

    forecasts = [
        item for item in data["list"]
        if datetime.fromtimestamp(item["dt"], tz=timezone.utc).date() == tomorrow
    ]
    return forecasts

if __name__ == "__main__":
    city = "Hanoi"
    print("🌤 Thời tiết hiện tại:")
    print(fetch_weather(city))

    print("\n📅 Dự báo ngày mai:")
    for f in fetch_forecast(city):
        dt_txt = datetime.fromtimestamp(f["dt"]).strftime("%Y-%m-%d %H:%M")
        print(f"{dt_txt}: {f['main']['temp']}°C, {f['weather'][0]['description']}")
