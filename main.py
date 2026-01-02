import os
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional

# Загружаем переменные окружения
load_dotenv()

from fastapi import FastAPI, HTTPException, Query

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
            "/convert-timezone": "Конвертировать время между часовыми поясами",
            "/timezones": "Получить список доступных часовых поясов",
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


# Словарь популярных часовых поясов с их IANA идентификаторами
TIMEZONE_MAPPING = {
    "moscow": "Europe/Moscow",
    "москва": "Europe/Moscow",
    "ekaterinburg": "Asia/Yekaterinburg",
    "екатеринбург": "Asia/Yekaterinburg",
    "yekaterinburg": "Asia/Yekaterinburg",
    "novosibirsk": "Asia/Novosibirsk",
    "новосибирск": "Asia/Novosibirsk",
    "krasnoyarsk": "Asia/Krasnoyarsk",
    "красноярск": "Asia/Krasnoyarsk",
    "irkutsk": "Asia/Irkutsk",
    "иркутск": "Asia/Irkutsk",
    "vladivostok": "Asia/Vladivostok",
    "владивосток": "Asia/Vladivostok",
    "magadan": "Asia/Magadan",
    "магадан": "Asia/Magadan",
    "kamchatka": "Asia/Kamchatka",
    "камчатка": "Asia/Kamchatka",
    "london": "Europe/London",
    "лондон": "Europe/London",
    "paris": "Europe/Paris",
    "париж": "Europe/Paris",
    "berlin": "Europe/Berlin",
    "берлин": "Europe/Berlin",
    "new_york": "America/New_York",
    "нью-йорк": "America/New_York",
    "los_angeles": "America/Los_Angeles",
    "лос-анджелес": "America/Los_Angeles",
    "chicago": "America/Chicago",
    "чикаго": "America/Chicago",
    "tokyo": "Asia/Tokyo",
    "токио": "Asia/Tokyo",
    "beijing": "Asia/Shanghai",
    "пекин": "Asia/Shanghai",
    "shanghai": "Asia/Shanghai",
    "шанхай": "Asia/Shanghai",
    "dubai": "Asia/Dubai",
    "дубай": "Asia/Dubai",
    "sydney": "Australia/Sydney",
    "сидней": "Australia/Sydney",
    "utc": "UTC",
}


@app.get("/convert-timezone")
async def convert_timezone(
    time: str = Query(..., description="Время в формате HH:MM или HH:MM:SS (например: 15:00)"),
    timezone: str = Query(..., description="Целевой часовой пояс (например: Екатеринбург, Moscow, UTC)"),
    from_timezone: str = Query("UTC", description="Исходный часовой пояс (по умолчанию UTC)")
):
    """
    Конвертирует время из одного часового пояса в другой
    
    Примеры:
    - /convert-timezone?time=15:00&timezone=Екатеринбург
    - /convert-timezone?time=15:00&timezone=Moscow&from_timezone=UTC
    - /convert-timezone?time=20:00&timezone=UTC&from_timezone=Ekaterinburg
    """
    try:
        # Парсим время
        time_parts = time.split(":")
        if len(time_parts) == 2:
            hour, minute = int(time_parts[0]), int(time_parts[1])
            second = 0
        elif len(time_parts) == 3:
            hour, minute, second = int(time_parts[0]), int(time_parts[1]), int(time_parts[2])
        else:
            raise ValueError("Неверный формат времени")
        
        if not (0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
            raise ValueError("Время вне допустимого диапазона")
        
        # Получаем IANA идентификаторы часовых поясов
        from_tz_key = from_timezone.lower().replace(" ", "_").replace("-", "_")
        to_tz_key = timezone.lower().replace(" ", "_").replace("-", "_")
        
        from_tz_name = TIMEZONE_MAPPING.get(from_tz_key, from_timezone)
        to_tz_name = TIMEZONE_MAPPING.get(to_tz_key, timezone)
        
        # Создаем datetime объект с исходным часовым поясом
        today = datetime.now().date()
        source_time = datetime(today.year, today.month, today.day, hour, minute, second)
        source_time = source_time.replace(tzinfo=ZoneInfo(from_tz_name))
        
        # Конвертируем в целевой часовой пояс
        target_time = source_time.astimezone(ZoneInfo(to_tz_name))
        
        return {
            "input": {
                "time": time,
                "timezone": from_timezone,
                "full_datetime": source_time.isoformat()
            },
            "output": {
                "time": target_time.strftime("%H:%M:%S"),
                "timezone": timezone,
                "timezone_name": to_tz_name,
                "full_datetime": target_time.isoformat(),
                "utc_offset": target_time.strftime("%z")
            },
            "time_difference": {
                "hours": (target_time.hour - source_time.hour) % 24,
                "description": f"Разница: {target_time.utcoffset().total_seconds() / 3600 - source_time.utcoffset().total_seconds() / 3600:+.0f} часов"
            }
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Ошибка формата времени: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Ошибка конвертации: {str(e)}. Используйте /timezones для списка доступных часовых поясов"
        )


@app.get("/timezones")
async def get_timezones():
    """Возвращает список доступных часовых поясов"""
    timezones_list = {}
    for key, value in TIMEZONE_MAPPING.items():
        if value not in timezones_list.values():
            timezones_list[key] = value
    
    return {
        "message": "Список доступных часовых поясов",
        "usage": "Используйте любое из этих названий в параметре 'timezone'",
        "timezones": timezones_list,
        "examples": [
            "/convert-timezone?time=15:00&timezone=Екатеринбург",
            "/convert-timezone?time=15:00&timezone=Moscow",
            "/convert-timezone?time=20:00&timezone=UTC&from_timezone=Ekaterinburg"
        ]
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

