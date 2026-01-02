# Time Server API

Приложение на FastAPI, простой тестовый бэкэнд, возвращающий текущее время сервера.


## Особенности приложения:

• **Настраиваемость**: все параметры (host, port, режим отладки) настраиваются через переменные окружения

• **Множественные форматы времени**: ISO формат, Unix timestamp, читаемый формат и часовой пояс

• **Автоматическая документация**: Swagger UI и ReDoc доступны по адресам /docs и /redoc

• **Проверка здоровья**: эндпоинт /health для мониторинга

## Для запуска:

1. Установите зависимости: `pip install -r requirements.txt`

2. Скопируйте `env.example` в `.env` и настройте параметры

3. Запустите: `python main.py`

Приложение будет доступно по адресу http://localhost:8000, а документация API - по http://localhost:8000/docs.

## Endpoints

- `GET /` - приветственное сообщение со списком доступных эндпоинтов
- `GET /time` - возвращает текущее время в различных форматах
- `GET /date` - возвращает текущую дату с подробной информацией
- `GET /date/year` - возвращает текущий год
- `GET /date/month` - возвращает текущий месяц
- `GET /date/day` - возвращает текущий день
- `GET /health` - проверка состояния сервера
- `GET /docs` - автоматическая документация (Swagger UI)
- `GET /redoc` - альтернативная документация (ReDoc)

## Примеры ответов

### GET /time

```json
{
  "current_time": "2026-01-02T15:30:45.123456",
  "timestamp": 1735826445.123456,
  "formatted_time": "2026-01-02 15:30:45",
  "timezone": "UTC+03:00"
}
```

### GET /date

```json
{
  "date": "2026-01-02",
  "year": 2026,
  "month": 1,
  "day": 2,
  "weekday": "Friday",
  "formatted_date": "02.01.2026"
}
```

### GET /date/year

```json
{
  "year": 2026
}
```

### GET /date/month

```json
{
  "month": 1,
  "month_name": "January",
  "month_name_ru": "January"
}
```

### GET /date/day

```json
{
  "day": 2,
  "weekday": "Friday",
  "day_of_year": 2
}
```

## Docker

### Сборка образа:
```bash
docker build -t time-server-api .
```

### Запуск контейнера:
```bash
docker run -d -p 8000:8000 --name time-server time-server-api
```

### Запуск с переменными окружения:
```bash
docker run -d -p 8000:8000 -e DEBUG=True --name time-server time-server-api
```

### Остановка контейнера:
```bash
docker stop time-server
```

### Удаление контейнера:
```bash
docker rm time-server
```

