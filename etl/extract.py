import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API")

def fetch_weather(city, lang="vi", units="metric"):
    """
    Gọi API OpenWeather để lấy dữ liệu thời tiết của city.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}&lang={lang}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
if __name__ == "__main__":
    print(fetch_weather("Hanoi"))