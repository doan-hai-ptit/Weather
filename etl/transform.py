from datetime import datetime, timezone, timedelta
def normalize_weather_data(data):
    """
    Chuẩn hoá dữ liệu JSON từ API để đưa vào DB.
    Trả về dict gọn gàng hơn.
    """
    VN_TZ = timezone(timedelta(hours=7))
    dt_vn = datetime.fromtimestamp(data["dt"], tz=VN_TZ)
    return {
        "dt": dt_vn,
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
def normalize_forecast_data(item, city_info):
    """
    Chuẩn hoá dữ liệu JSON của 1 bản ghi từ API /forecast để đưa vào DB.
    Bao gồm cả thông tin thành phố, quốc gia, toạ độ,...
    """
    VN_TZ = timezone(timedelta(hours=7))
    dt_vn = datetime.fromtimestamp(item["dt"], tz=VN_TZ)

    coord = city_info.get("coord", {"lat": None, "lon": None})

    return {
        "dt": dt_vn,  # thời điểm dự báo (future)
        "city_name": city_info.get("name"),
        "country": city_info.get("country"),
        "lat": coord.get("lat"),
        "lon": coord.get("lon"),
        "temp": item["main"]["temp"],
        "feels_like": item["main"]["feels_like"],
        "humidity": item["main"]["humidity"],
        "wind_speed": item.get("wind", {}).get("speed"),
        "weather_main": item["weather"][0]["main"],
        "weather_desc": item["weather"][0]["description"],
        "visibility": item.get("visibility"),
        "raw": item  # dữ liệu gốc để debug nếu cần
    }