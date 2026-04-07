import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 1. Tải các biến môi trường từ file .env
load_dotenv()

# 2. Khởi tạo LLM với cấu hình OpenRouter
# Nhớ đảm bảo trong file .env đã có OPENROUTER_API_KEY
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:3000", # URL ứng dụng 
        "X-Title": "TravelBuddy Lab"             # Tên ứng dụng hiển thị trên OpenRouter
    }
)

# 3. Kiểm tra thử
try:
    response = llm.invoke("Xin chào?")
    print(response.content)
except Exception as e:
    print(f"Ôi không, có lỗi rồi: {e}")