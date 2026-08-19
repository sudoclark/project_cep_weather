import requests
import os
from dotenv import load_dotenv
from flask import request as FlaskRequest
from typing import Dict

from src.main.errors.http_not_found import NotFoundError
from src.main.errors.http_badrequest import HttpBadRequestError
from src.main.errors.api_key_error import ApiKeyError

load_dotenv()


class GetWeather:
    WEATHER_API_KEY = os.getenv('API_KEY')

    def get_weather(self, request: FlaskRequest) -> None: # type: ignore
        """
        Método público que serve como 'interface' do processamento. Chama os métodos internos, cada um
        com sua responsabilidade.
        """
        body = request.json
        cep = self.__validate_body_request(body)
        city = self.__city_discovery(cep)

        weather_info = self.__weather_discovery(city)

        return weather_info

    def __validate_body_request(self, body: Dict) -> int:
        """
        Valida o corpo da requisição. A request chega com um único campo 'cep'. Esse método valida
        se esse campo está presente no body.
        """
        if "cep" not in body:
            raise HttpBadRequestError("Dados incorretos, verifique os campos enviados.")

        cep = body["cep"]

        return cep

    def __city_discovery(self, cep: int) -> str:
        """
        Método para descobrir o nome da cidade do cep informado. Chama uma API externa chamada 'viacep'.
        Essa API retorna diversas informações atreladas a um cep específico.
        """
        if " " in str(cep):
            raise HttpBadRequestError("O cep não deve conter espaços.")
        
        if not isinstance(cep, int):
            raise HttpBadRequestError("O cep fornecido deve ser um número.")

        response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        response_data = response.json()

        if "erro" in response_data:
            raise HttpBadRequestError("Dados inválidos, verifique o cep enviado.")

        city = response_data["localidade"]

        return city

    def __weather_discovery(self, city: str) -> Dict:
        """
        Método para descobrirmos o clima atual de uma cidade. Chama uma API externa que nos retorna diversas informações
        climáticas sobre uma cidade específica.
        Eu busco as informações, filtro as mais importantes e retorno esse dicionário processado.
        """

        # 'units=metric' converte os graus de kelvin para celsius e o lang='pt-br' traduz o campo 'description' para português.
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.WEATHER_API_KEY}&units=metric&lang={'pt_br'}")
        response_data = response.json()

        if "cod" == "401":
            raise ApiKeyError("API_KEY incorreta, verifique os dados")

        if "cod" == "404":
            raise NotFoundError("Cidade não encontrada, verifique as informações enviadas")

        weather = response_data["weather"][0]["main"]
        description = response_data["weather"][0]["description"]
        tempeture = response_data["main"]["temp"]
        wind_velocity = response_data["wind"]["speed"]

        city_weather_info = {
            "city": city,
            "weather": weather,
            "description": description,
            "tempeture": tempeture,
            "wind_velocity": wind_velocity
        }

        return city_weather_info