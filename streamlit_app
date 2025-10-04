import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from db.db_utils import get_weather_by_city, get_forecast_by_city, get_all_city
from etl import run_pipeline, run_forecast_pipeline
import platform

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
# Ba nút trên cùng một hàng
col1, col2, col3 = st.columns(3)

show_weather = False
update_data = False
collect_forecast = False

with col1:
    if st.button("☀️ Xem thời tiết hôm nay"):
        show_weather = True

with col2:
    if st.button("🔄 Cập nhật dữ liệu hôm nay"):
        update_data = True

with col3:
    if st.button("🌤️ Thu thập dự báo ngày mai"):
        collect_forecast = True

# ---------------------------------------------------
# Cập nhật dữ liệu hiện tại
if update_data:
    with st.spinner("Đang cập nhật dữ liệu thời tiết hôm nay..."):
        for c in city_list:
            run_pipeline(c)
    st.success("✅ Đã cập nhật dữ liệu hôm nay xong!")

# ---------------------------------------------------
# Thu thập dữ liệu dự báo
if collect_forecast:
    if city:
        forecast_df = get_forecast_by_city(str(city))
        if forecast_df.empty:
            with st.spinner(f"Đang thu thập dữ liệu dự báo 3h/lần cho {city}..."):
                run_forecast_pipeline(city)
            st.success(f"✅ Đã thu thập và lưu dự báo thời tiết ngày mai cho {city}!")
        else:
            st.info(f"ℹ️ Dữ liệu dự báo cho {city} đã tồn tại trong DB, không cần thu thập lại.")
    else:
        st.warning("⚠️ Vui lòng chọn thành phố trước.")

# ---------------------------------------------------
if show_weather and city:
    # 🟢 1️⃣ Thời tiết hiện tại (bảng fact_weather)
    current_df = get_weather_by_city(str(city))
    if not current_df.empty:
        st.subheader(f"☀️ Thời tiết hiện tại tại {city}")
        row = current_df.iloc[0]
        st.write(f"**Nhiệt độ:** {row['temperature']}°C")
        st.write(f"**Độ ẩm:** {row['humidity']}%")
        st.write(f"**Tốc độ gió:** {row['wind_speed']} m/s")
        st.write(f"**Mô tả:** {row['weather_desc']}")

        # --- Biểu đồ thời tiết trong ngày hôm nay ---
        st.markdown("### 📊 Biểu đồ thay đổi thời tiết hôm nay")
        current_df["time"] = pd.to_datetime(current_df["dt"]).dt.strftime("%H:%M")

        cols = st.columns(3)
        charts = [
            ("🌡️ Nhiệt độ", "temperature", "°C", "red", "o"),
            ("💧 Độ ẩm", "humidity", "%", "blue", "s"),
            ("💨 Tốc độ gió", "wind_speed", "m/s", "green", "^"),
        ]

        for (title, colname, ylabel, color, marker), col in zip(charts, cols):
            with col:
                fig, ax = plt.subplots(figsize=(4, 4))
                ax.plot(current_df["time"], current_df[colname], marker=marker, color=color)
                ax.set_title(title)
                ax.set_xlabel("Giờ")
                ax.set_ylabel(ylabel)
                ax.grid(True)
                st.pyplot(fig)
    else:
        st.warning("Không tìm thấy dữ liệu thời tiết hôm nay trong DB.")

    # 🟡 2️⃣ Dự báo theo giờ (bảng fact_weather_forecast_hourly)
    forecast_df = get_forecast_by_city(str(city))

    st.markdown("### 🌤️ Dự báo theo giờ ngày mai")
    if not forecast_df.empty:
        st.dataframe(forecast_df)

        if platform.system() == "Windows":
            forecast_df["time"] = pd.to_datetime(forecast_df["dt"]).dt.strftime("%#Hh")
        else:
            forecast_df["time"] = pd.to_datetime(forecast_df["dt"]).dt.strftime("%-Hh")


        cols = st.columns(3)
        charts = [
            ("🌡️ Nhiệt độ dự báo", "temperature", "°C", "red", "o"),
            ("💧 Độ ẩm dự báo", "humidity", "%", "blue", "s"),
            ("💨 Gió dự báo", "wind_speed", "m/s", "green", "^"),
        ]

        for (title, colname, ylabel, color, marker), col in zip(charts, cols):
            with col:
                fig, ax = plt.subplots(figsize=(4, 4))
                ax.plot(forecast_df["time"], forecast_df[colname], marker=marker, color=color)
                ax.set_title(title)
                ax.set_xlabel("Giờ (VN)")
                ax.set_ylabel(ylabel)
                ax.grid(True)
                st.pyplot(fig)
    else:
        st.info("⏳ Chưa có dữ liệu dự báo trong DB. Hãy nhấn 🌤️ **Thu thập dự báo ngày mai**.")
