from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from app import db
from app.models import User, Country, SeasonFactor
from app.services import calculate_total_cost

main_bp = Blueprint('main', __name__)

# Главная страница
@main_bp.route('/')
def index():
    countries = Country.query.all()  # Загружаем все страны из базы данных
    seasons = SeasonFactor.query.all()  # Загружаем все сезоны из базы данных
    message = session.get('message', None)  # Получаем сообщение об ошибке
    session.pop('message', None)  # Удаляем сообщение после показа
    return render_template('index.html', message=message, countries=countries, seasons=seasons)

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
