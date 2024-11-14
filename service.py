from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import Swagger

app = Flask(__name__, template_folder='app/templates')
app.secret_key = 'your_secret_key'  # Не забудьте установить секретный ключ для работы сессий

# Инициализация Swagger для документации
swagger = Swagger(app, template_file='swagger.yml')

# Пример базы данных пользователей (для лабораторной работы можно использовать в памяти)
users_db = {}
base_cost = {
        "USA": {"flight": 600, "accommodation": 150, "food": 30, "transport": 20},
        "France": {"flight": 500, "accommodation": 200, "food": 25, "transport": 15},
        "Japan": {"flight": 800, "accommodation": 250, "food": 35, "transport": 25}
    }
seasonal_factors = {
    "summer": 1.2,
    "winter": 1.5,
    "offseason": 1.0
}

# Главная страница для рендеринга HTML
@app.route('/')
def index():
    message = session.get('message', None)
    session.pop('message', None)  # Удаляем сообщение после показа
    return render_template('index.html', message=message)

# Регистрация пользователя
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    
    # Проверка, если пользователь уже существует
    if username in users_db:
        return jsonify({"error": "Пользователь уже существует"}), 400
    
    # Хеширование пароля
    hashed_password = generate_password_hash(password)
    
    # Сохраняем пользователя
    users_db[username] = hashed_password
    
    # Логиним пользователя после регистрации
    session['user'] = username
    session['message'] = "Регистрация успешна!"
    print(session['user'])

    
    return jsonify({"message": "Регистрация успешна", "username": username})

# Вход пользователя
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    # Проверка существования пользователя
    if username not in users_db:
        return jsonify({"error": "Пользователь не найден"}), 400
    
    # Проверка пароля
    if not check_password_hash(users_db[username], password):
        return jsonify({"error": "Неверный пароль"}), 400
    
    # Устанавливаем сессию для пользователя
    session['user'] = username
    
    return jsonify({"message": "Вход успешен", "username": username})

# Выйти из аккаунта
@app.route('/logout')
def logout():
    session.pop('user', None)  # Удалить пользователя из сессии
    return jsonify({"message": "Выход успешен"}), 200

# API для расчета стоимости поездки
@app.route('/api/calculate_trip_cost', methods=['POST'])
def calculate_trip_cost():
    # Проверка, авторизован ли пользователь
    if 'user' not in session:
        return jsonify({"error": "Пользователь не авторизован"}), 401

    # Получаем данные из запроса
    data = request.json
    country = data['country']
    season = data['season']
    duration = data['duration']
    additional_expenses = data['additional_expenses']
    num_people = data['num_people']
    
    # Проверка наличия страны в базе
    if country not in base_cost:
        return jsonify({"error": "Страна не поддерживается"}), 400

    if season not in seasonal_factors:
        return jsonify({"error": "Сезон не поддерживается"}), 400
    
    # Преобразуем все входные данные в нужные типы данных
    try:
        num_people = int(num_people)
        duration = int(duration)
        additional_expenses = float(additional_expenses)
    except ValueError as e:
        return jsonify({"error": "Некорректные данные"}), 400
    
    # Вычисление стоимости
    flight_cost = float(base_cost[country]["flight"]) * seasonal_factors[season] * num_people
    accommodation_cost = float(base_cost[country]["accommodation"]) * duration * num_people
    food_cost = float(base_cost[country]["food"]) * duration * num_people
    transport_cost = float(base_cost[country]["transport"]) * duration * num_people
    
    # Пример групповой скидки
    discount = 0
    if num_people > 2:
        discount = 0.1 * transport_cost
        max_discount = 25  # Максимальная сумма скидки
        discount = min(discount, max_discount)
        print(discount)

    total_cost = (flight_cost + accommodation_cost + food_cost + transport_cost +
                  additional_expenses - discount)
    
    return jsonify({
        "total_cost": total_cost,
        "breakdown": {
            "flight": flight_cost,
            "accommodation": accommodation_cost,
            "food": food_cost,
            "transport": transport_cost,
            "activities": additional_expenses,
            "discount": discount
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
