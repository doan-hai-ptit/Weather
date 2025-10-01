import streamlit as st
import pandas as pd
from db.connection import get_engine

st.set_page_config(page_title="Weather Data", page_icon="⛅")

def load_data(limit=20):
    engine = get_engine()
    query = f"""
        SELECT c.city_name, f.temperature, f.feels_like, 
               f.humidity, f.wind_speed, f.weather_desc, f.dt
        FROM fact_weather f
        JOIN dim_city c ON f.city_id = c.city_id
        ORDER BY f.dt DESC
        LIMIT {limit};
    """
    df = pd.read_sql(query, engine)
    return df

st.title("📊 Weather Fact Table Viewer")

limit = st.slider("Số dòng muốn xem:", 5, 100, 20)
df = load_data(limit)

# Hiển thị dạng bảng
st.dataframe(df, use_container_width=True)

# Hiển thị từng bản ghi dạng "card"
st.subheader("🌍 Chi tiết thời tiết")
for _, row in df.iterrows():
    with st.container():
        st.markdown(f"""
        **Thành phố:** {row['city_name']}  
        - 🌡️ Nhiệt độ: {row['temperature']}°C (cảm giác {row['feels_like']}°C)  
        - ☁️ Trạng thái: {row['weather_desc']}  
        - 💧 Độ ẩm: {row['humidity']}%  
        - 💨 Gió: {row['wind_speed']} m/s  
        - 🕒 Thời gian: {row['dt']}
        """)
        st.markdown("---")
