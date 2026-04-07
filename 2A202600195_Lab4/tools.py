from langchain_core.tools import tool
from typing import Dict, List, Optional

# MOCK DATA
FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1450000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2800000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1200000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2100000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1350000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1100000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1600000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1300000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3200000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1300000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1100000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650000, "class": "economy"},
    ]
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1800000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1200000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3500000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1500000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2800000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1400000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180000, "area": "Quận 1", "rating": 4.6},
    ]
}

@tool
def search_flights(origin: str, destination: str) -> str:
    """Tìm kiếm các chuyến bay giữa hai thành phố."""
    flights = FLIGHTS_DB.get((origin, destination))
    if not flights:
        # Thử tra ngược chiều
        flights = FLIGHTS_DB.get((destination, origin))
        if not flights:
            return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."
    
    res = f"Danh sách chuyến bay {origin} - {destination}:\n"
    for f in flights:
        res += f"- {f['airline']} ({f['departure']}-{f['arrival']}): {f['price']:,}đ [{f['class']}]\n"
    return res

@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa."""
    hotels = HOTELS_DB.get(city, [])
    filtered = [h for h in hotels if h['price_per_night'] <= max_price_per_night]
    filtered.sort(key=lambda x: x['rating'], reverse=True)
    
    if not filtered:
        return f"Không tìm thấy khách sạn tại {city} với giá dưới {max_price_per_night:,}đ/đêm."
    
    res = f"Khách sạn tại {city} (Ưu tiên đánh giá cao):\n"
    for h in filtered:
        res += f"- {h['name']} ({h['stars']}*): {h['price_per_night']:,}đ/đêm - Khu vực: {h['area']} (Rating: {h['rating']})\n"
    return res

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """Tính toán ngân sách còn lại. Expenses format: 'tên_khoản:số_tiền,tên_khoản:số_tiền'"""
    try:
        items = expenses.split(',')
        total_spent = 0
        breakdown = ""
        for item in items:
            name, price = item.split(':')
            price = int(price.strip())
            total_spent += price
            breakdown += f"- {name.strip()}: {price:,}đ\n"
        
        remaining = total_budget - total_spent
        status = f"Còn lại: {remaining:,}đ" if remaining >= 0 else f"Vượt ngân sách: {abs(remaining):,}đ! Cần điều chỉnh."
        
        return f"Bảng chi phí:\n{breakdown}---\nTổng chi: {total_spent:,}đ\nNgân sách: {total_budget:,}đ\n{status}"
    except Exception:
        return "Lỗi định dạng expenses. Vui lòng dùng định dạng 'item:price,item:price'."