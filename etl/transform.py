from datetime import datetime
def normalize_weather_data(data):
    """
    Chuẩn hoá dữ liệu JSON từ API để đưa vào DB.
    Trả về dict gọn gàng hơn.
    """
    return {
        "dt": datetime.utcfromtimestamp(data["dt"]),
        "city_name": data["name"],
        "country": data["sys"]["country"],
        "lat": data["coord"]["lat"],
        "lon": data["coord"]["lon"],
        "temp": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data.get("wind", {}).get("speed"),
        "weather_main": data["weather"][0]["main"],
        "weather_desc": data["weather"][0]["description"],
        "visibility": data["visibility"],
        "raw": data
    }
