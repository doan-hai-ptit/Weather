from etl import run_pipeline, run_forecast_pipeline

city_list = [
    "Hanoi,VN",                # Hà Nội
    "Ho Chi Minh City,VN",     # TP.HCM
    "Haiphong,VN",             # Hải Phòng
    "Da Nang,VN",              # Đà Nẵng
    "Can Tho,VN",              # Cần Thơ
    "An Giang,VN",             # Long Xuyên
    "Vung Tau,VN",             # Bà Rịa - Vũng Tàu
    "Bac Giang,VN",            # Bắc Giang
    "Bac Kan,VN",              # Bắc Kạn
    "Bac Lieu,VN",             # Bạc Liêu
    "Bac Ninh,VN",             # Bắc Ninh
    "Ben Tre,VN",              # Bến Tre
    "Quy Nhon,VN",             # Bình Định
    "Thu Dau Mot,VN",          # Bình Dương
    "Dong Xoai,VN",            # Bình Phước
    "Phan Thiet,VN",           # Bình Thuận
    "Ca Mau,VN",               # Cà Mau
    "Cao Bang,VN",             # Cao Bằng
    "Buon Ma Thuot,VN",        # Đắk Lắk
    "Dien Bien Phu,VN",        # Điện Biên
    "Bien Hoa,VN",             # Đồng Nai
    "Cao Lanh,VN",             # Đồng Tháp
    "Pleiku,VN",               # Gia Lai
    "Ha Giang,VN",             # Hà Giang
    "Phu Ly,VN",               # Hà Nam
    "Ha Tinh,VN",              # Hà Tĩnh
    "Hai Duong,VN",            # Hải Dương
    "Vi Thanh,VN",             # Hậu Giang
    "Hoa Binh,VN",             # Hòa Bình
    "Hung Yen,VN",             # Hưng Yên
    "Nha Trang,VN",            # Khánh Hòa
    "Rach Gia,VN",             # Kiên Giang
    "Kon Tum,VN",              # Kon Tum
    "Lai Chau,VN",             # Lai Châu
    "Da Lat,VN",               # Lâm Đồng
    "Lang Son,VN",             # Lạng Sơn
    "Lao Cai,VN",              # Lào Cai
    "Tan An,VN",               # Long An
    "Nam Dinh,VN",             # Nam Định
    "Vinh,VN",                 # Nghệ An
    "Ninh Binh,VN",            # Ninh Bình
    "Phan Rang-Thap Cham,VN",  # Ninh Thuận
    "Viet Tri,VN",             # Phú Thọ
    "Tuy Hoa,VN",              # Phú Yên
    "Dong Hoi,VN",             # Quảng Bình
    "Tam Ky,VN",               # Quảng Nam
    "Quang Ngai,VN",           # Quảng Ngãi
    "Ha Long,VN",              # Quảng Ninh
    "Dong Ha,VN",              # Quảng Trị
    "Soc Trang,VN",            # Sóc Trăng
    "Son La,VN",               # Sơn La
    "Tay Ninh,VN",             # Tây Ninh
    "Thai Binh,VN",            # Thái Bình
    "Thai Nguyen,VN",          # Thái Nguyên
    "Thanh Hoa,VN",            # Thanh Hóa
    "Hue,VN",                  # Thừa Thiên - Huế
    "My Tho,VN",               # Tiền Giang
    "Tra Vinh,VN",             # Trà Vinh
    "Tuyen Quang,VN",          # Tuyên Quang
    "Vinh Long,VN",            # Vĩnh Long
    "Vinh Yen,VN",             # Vĩnh Phúc
    "Yen Bai,VN"               # Yên Bái
]

if __name__ == "__main__":
    for i in city_list:
        # run_pipeline(i)
        run_forecast_pipeline(i)