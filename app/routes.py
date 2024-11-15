from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, Country, SeasonFactor
from app.services import calculate_total_cost

main_bp = Blueprint('main', __name__)

# Главная страница
@main_bp.route('/')
def index():
    countries = Country.query.all()  # Загружаем все страны из базы данных
    seasons = SeasonFactor.query.all()  # Загружаем все сезоны из базы данных
    print(countries)
    print(seasons)
    message = session.get('message', None)
    session.pop('message', None)  # Удаляем сообщение после показа
    return render_template('index.html', message=message, countries=countries, seasons=seasons)

# Регистрация пользователя
@main_bp.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    # Проверка существования пользователя в БД
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Пользователь уже существует"}), 400

    # Создаем пользователя и сохраняем в БД
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    session['user'] = username
    session['message'] = "Регистрация успешна!"
    return jsonify({"message": "Регистрация успешна", "username": username})

# Вход пользователя
@main_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Проверка пользователя в БД
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Неверное имя пользователя или пароль"}), 400

    session['user'] = username
    return jsonify({"message": "Вход успешен", "username": username})

# Выйти из аккаунта
@main_bp.route('/logout')
def logout():
    session.pop('user', None)
    return jsonify({"message": "Выход успешен"}), 200

# API для расчета стоимости поездки
@main_bp.route('/api/calculate_trip_cost', methods=['POST'])
def calculate_trip_cost():

    data = request.json
    total_cost, breakdown = calculate_total_cost(data)

    if not total_cost:
        return jsonify({"error": "Ошибка в данных"}), 400

    return jsonify({
        "total_cost": total_cost,
        "breakdown": breakdown
    })
