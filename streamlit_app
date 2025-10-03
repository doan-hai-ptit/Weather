import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta, timezone
from db.db_utils import get_weather_by_city, get_all_weather_by_city, get_all_city
from etl import run_pipeline

st.set_page_config(page_title="Weather Forecast", layout="wide")
st.title("🌦️ Ứng dụng dự báo thời tiết (dữ liệu từ DB)")

# ---------------------------------------------------
# Hiển thị phần chọn thành phố
city_name_df = get_all_city()
city_list = city_name_df["city_name"].tolist() if not city_name_df.empty else []

if city_list:
    city = st.selectbox("Chọn thành phố:", city_list, index=0)
else:
    st.warning("⚠️ Không có dữ liệu thành phố trong database")
    city = None

# ---------------------------------------------------
# Hai nút trên cùng một hàng
col1, col2 = st.columns(2)

show_weather = False  # biến cờ
update_data = False

with col1:
    if st.button("Xem thời tiết"):
        show_weather = True

with col2:
    if st.button("🔄 Cập nhật dữ liệu"):
        update_data = True

# ---------------------------------------------------
# Xử lý nút bấm
if update_data:
    with st.spinner("Đang cập nhật dữ liệu thời tiết..."):
        for c in city_list:
            run_pipeline(c)
    st.success("✅ Đã cập nhật dữ liệu xong!")

if show_weather and city:
    current_df = get_weather_by_city(str(city))

    if not current_df.empty:
        st.subheader(f"☀️ Thời tiết hiện tại tại {city}")
        row = current_df.iloc[0]
        st.write(f"Nhiệt độ: {row['temperature']}°C")
        st.write(f"Độ ẩm: {row['humidity']}%")
        st.write(f"Tốc độ gió: {row['wind_speed']} m/s")
        st.write(f"Mô tả: {row['weather_desc']}")
    else:
        st.warning("Không tìm thấy dữ liệu trong DB.")
        st.stop()

    forecast_df = get_all_weather_by_city(str(city))

    st.subheader(f"📅 Biểu đồ thay đổi tại {city}")
    st.dataframe(forecast_df)

    if not forecast_df.empty:
        forecast_df["time"] = pd.to_datetime(forecast_df["dt"]).dt.strftime("%m-%d")

        # tạo 3 biểu đồ ngang hàng
        cols = st.columns(3)
        charts = [
            ("Nhiệt độ", "temperature", "°C", "red", "o"),
            ("Độ ẩm", "humidity", "%", "blue", "s"),
            ("Tốc độ gió", "wind_speed", "m/s", "green", "^"),
        ]

        for (title, colname, ylabel, color, marker), col in zip(charts, cols):
            with col:
                fig, ax = plt.subplots(figsize=(4, 4))
                ax.plot(forecast_df["time"], forecast_df[colname], marker=marker, color=color)
                ax.set_title(title)
                ax.set_xlabel("Ngày")
                ax.set_ylabel(ylabel)
                ax.grid(True)
                st.pyplot(fig)
