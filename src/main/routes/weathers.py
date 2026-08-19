from flask import Blueprint, request, jsonify

from src.services.get_weather import GetWeather
from src.main.errors.error_handler import handler_error

weather_bp_routes = Blueprint("weather_bp", __name__)

@weather_bp_routes.route("/weather_discovery", methods=["POST"])
def city_weather_discovery():
    """
    Rota para descobrirmos o clima de uma cidade baseado no CEP.

        Recebe: Um dicionário no formato {'cep': 99999999} (CEP é um inteiro)
        Retorna: Um novo dicionário com as informações climáticas

    Possui tratamento de erro com o objetivo de deixar mais informativo e assertivo para o usuário.
    """
    try:
        weather_service = GetWeather()
        response = weather_service.get_weather(request)

        return jsonify(response)

    except Exception as ex:
        error = handler_error(ex)
        return jsonify(error["data"]), error["status_code"]