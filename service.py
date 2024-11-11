from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)

# Укажите путь к вашему YAML файлу
swagger = Swagger(app, template_file='swagger.yml')

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

@app.route('/api/calculate_trip_cost', methods=['POST'])
def calculate_trip_cost():
    data = request.json
    country = data['country']
    season = data['season']
    duration = data['duration']
    additional_expenses = data['additional_expenses']
    num_people = data['num_people']
    
    if country not in base_cost:
        return jsonify({"error": "Страна не поддерживается"}), 400

    if season not in seasonal_factors:
        return jsonify({"error": "Сезон не поддерживается"}), 400
    
    flight_cost = base_cost[country]["flight"] * seasonal_factors[season] * num_people
    accommodation_cost = base_cost[country]["accommodation"] * duration * num_people
    food_cost = base_cost[country]["food"] * duration * num_people
    transport_cost = base_cost[country]["transport"] * duration * num_people
    
    # Пример групповой скидки
    discount = 0
    if num_people > 2:
        discount = 0.1 * (flight_cost + accommodation_cost + food_cost + transport_cost + additional_expenses)

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

@app.route('/api/get_trip_cost_info', methods=['GET'])
def get_trip_cost_info():
    country = request.args.get('country')
    season = request.args.get('season')

    if country not in base_cost:
        return jsonify({"error": "Страна не поддерживается"}), 400
    
    if season not in seasonal_factors:
        return jsonify({"error": "Сезон не поддерживается"}), 400

    cost_info = {
        "country": country,
        "season": season,
        "flight_cost": base_cost[country]["flight"] * seasonal_factors[season],
        "accommodation_cost": base_cost[country]["accommodation"],
        "food_cost": base_cost[country]["food"],
        "transport_cost": base_cost[country]["transport"]
    }

    return jsonify(cost_info)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
