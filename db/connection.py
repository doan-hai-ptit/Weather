import psycopg2
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()  # load biến môi trường từ file .env nếu có

def get_connection():
    """
    Trả về connection đến PostgreSQL.
    Lấy thông tin từ biến môi trường trong .env
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            port=os.getenv("DB_PORT")
        )
        return conn
    except Exception as e:
        print("❌ Không thể kết nối đến PostgreSQL:", e)
        raise

def get_engine():
    """
    Trả về SQLAlchemy engine (dùng cho pandas.read_sql).
    """
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_PORT = os.getenv("DB_PORT")

    url = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url)
def test_connection():
    try:
        conn = get_connection()
        print("✅ Kết nối thành công tới PostgreSQL")
        conn.close()
    except Exception as e:
        print("❌ Lỗi khi test kết nối:", e)


# Nếu chạy trực tiếp file thì test luôn
if __name__ == "__main__":
    test_connection()
