import os
from dotenv import load_dotenv
from datetime import datetime

# Загружаем переменные окружения
load_dotenv()

from fastapi import FastAPI

app = FastAPI(
    title="Time Server API",
    description="Простое API для получения текущего времени сервера",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Корневой эндпоинт с приветствием"""
    return {
        "message": "Добро пожаловать в Time Server API!",
        "endpoints": {
            "/time": "Получить текущее время",
            "/date": "Получить текущую дату",
            "/date/year": "Получить текущий год",
            "/date/month": "Получить текущий месяц",
            "/date/day": "Получить текущий день",
            "/health": "Проверка состояния сервера",
            "/docs": "Документация API"
        }
    }


@app.get("/time")
async def get_current_time():
    """Возвращает текущее время сервера"""
    current_time = datetime.now()
    return {
        "current_time": current_time.isoformat(),
        "timestamp": current_time.timestamp(),
        "formatted_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": str(current_time.astimezone().tzinfo())
    }


@app.get("/date")
async def get_current_date():
    """Возвращает текущую дату сервера"""
    current_date = datetime.now()
    return {
        "date": current_date.date().isoformat(),
        "year": current_date.year,
        "month": current_date.month,
        "day": current_date.day,
        "weekday": current_date.strftime("%A"),
        "formatted_date": current_date.strftime("%d.%m.%Y")
    }


@app.get("/date/year")
async def get_current_year():
    """Возвращает текущий год"""
    return {"year": datetime.now().year}


@app.get("/date/month")
async def get_current_month():
    """Возвращает текущий месяц"""
    current_date = datetime.now()
    return {
        "month": current_date.month,
        "month_name": current_date.strftime("%B"),
        "month_name_ru": current_date.strftime("%B")
    }


@app.get("/date/day")
async def get_current_day():
    """Возвращает текущий день"""
    current_date = datetime.now()
    return {
        "day": current_date.day,
        "weekday": current_date.strftime("%A"),
        "day_of_year": current_date.timetuple().tm_yday
    }


@app.get("/health")
async def health_check():
    """Проверка состояния сервера"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    # Получаем настройки из переменных окружения
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    import uvicorn
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug
    )

