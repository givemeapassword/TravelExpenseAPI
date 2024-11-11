# TravelExpenseAPI

Этот проект представляет собой **Flask** приложение с API для расчёта общей стоимости поездки, включая стоимость авиабилетов, проживания, питания, транспорта и дополнительных расходов, с учётом сезонных коэффициентов. Он также позволяет получить информацию о стоимости по выбранной стране и сезону.

Проект включает:
- **POST** эндпоинт для расчёта полной стоимости поездки с учётом всех факторов.
- **GET** эндпоинт для получения информации о стоимости для выбранной страны и сезона.
- **Swagger UI** для удобного взаимодействия с API.

## Особенности

- **Динамическая настройка стоимости**: Используются сезонные коэффициенты, которые могут менять стоимость в зависимости от сезона (лето, зима, межсезонье).
- **Групповые скидки**: Для группы из более чем двух человек предусмотрены скидки.
- **Документация через Swagger UI**: Интерактивное API, где можно протестировать все эндпоинты.
- **Простой и понятный интерфейс**: Swagger UI позволяет легко отправлять запросы и получать ответы.

## Как это работает?

### 1. Эндпоинт `/api/calculate_trip_cost` (POST)
Этот эндпоинт рассчитывает полную стоимость поездки. Вам нужно передать:
- Страну назначения
- Сезон поездки
- Продолжительность поездки
- Дополнительные расходы
- Количество людей в группе

Пример запроса:
```json
{
  "country": "USA",
  "season": "summer",
  "duration": 7,
  "additional_expenses": 300,
  "num_people": 4
}
```

Пример ответа:

```json
{
  "total_cost": 8700.0,
  "breakdown": {
    "flight": 2400.0,
    "accommodation": 1400.0,
    "food": 420.0,
    "transport": 280.0,
    "activities": 300.0,
    "discount": 200.0
  }
}
```


### 2. /api/get_trip_cost_info (GET)

Этот эндпоинт позволяет получить информацию о стоимости основных категорий расходов для выбранной страны и сезона.


Пример запроса:

```bash
GET /api/get_trip_cost_info?country=USA&season=summer
```

Пример ответа:
```json
{
  "country": "USA",
  "season": "summer",
  "flight_cost": 800.0,
  "accommodation_cost": 150.0,
  "food_cost": 30.0,
  "transport_cost": 20.0
}
```
## Установка и запуск
### 1. Клонируйте репозиторий
```bash
git clone https://github.com/your-username/trip-cost-api.git
cd trip-cost-api
```
### 2. Установите зависимости
Для установки зависимостей используйте pip:
```bash
pip install -r requirements.txt
```
### 3. Запустите приложение
Чтобы запустить сервер, используйте команду:
```bash
python app.py
```
После этого сервер будет доступен по адресу `http://localhost:5000`.

### 4. Тестирование API через Swagger UI
Откройте браузер и перейдите по адресу `http://localhost:5000/apidocs`, чтобы протестировать API через Swagger UI. Вы сможете отправлять запросы и получать ответы непосредственно в браузере.

## Зависимости
Проект использует следующие библиотеки:

Flask: Для создания веб-приложения

Flasgger: Для интеграции с Swagger UI и генерации документации API
