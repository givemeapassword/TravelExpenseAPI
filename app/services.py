from app.models import Country, SeasonFactor

def calculate_total_cost(data):
    country = data['country']
    season = data['season']
    duration = int(data['duration'])
    additional_expenses = float(data['additional_expenses'])
    num_people = int(data['num_people'])

    country_data = Country.query.filter_by(country_name=country).first()
    season_factor = SeasonFactor.query.filter_by(season=season).first()

    if not country_data or not season_factor:
        return None, None

    # Вычисление стоимости
    flight_cost = country_data.flight * season_factor.factor * num_people
    accommodation_cost = country_data.accommodation * duration * num_people
    food_cost = country_data.food * duration * num_people
    transport_cost = country_data.transport * duration * num_people

    discount = 0
    if num_people > 2:
        discount = min(0.1 * transport_cost, 25)

    total_cost = flight_cost + accommodation_cost + food_cost + transport_cost + additional_expenses - discount

    return total_cost, {
        "flight": flight_cost,
        "accommodation": accommodation_cost,
        "food": food_cost,
        "transport": transport_cost,
        "activities": additional_expenses,
        "discount": discount
    }
