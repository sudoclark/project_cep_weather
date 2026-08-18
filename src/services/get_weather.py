import requests
import os
from dotenv import load_dotenv
from flask import request as FlaskRequest
from typing import Dict

load_dotenv()


class GetWeather:
    WEATHER_API_KEY = os.getenv('API_KEY')

    def get_weather(self, request: FlaskRequest) -> None: # type: ignore
        body = request.json
        cep = self.__validate_body_request(body)
        city = self.__city_discovery(cep)

        weather_info = self.__weather_discovery(city)

        return weather_info

    def __validate_body_request(self, body: Dict) -> int:
        if "cep" not in body:
            raise Exception("Dados incorretos, verifique os campos enviados.")

        cep = body["cep"]

        return cep

    def __city_discovery(self, cep: int) -> str:
        if " " in str(cep):
            raise Exception("O cep não deve conter espaços.")
        
        if not isinstance(cep, int):
            raise Exception("O cep fornecido deve ser um número.")

        response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        response_data = response.json()

        if "erro" in response_data:
            raise Exception("Dados inválidos, verifique o cep enviado.")

        city = response_data["localidade"]

        return city

    def __weather_discovery(self, city: str) -> Dict:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.WEATHER_API_KEY}&units=metric&lang={'pt_br'}")
        response_data = response.json()

        if "cod" == "401":
            raise Exception("API_KEY incorreta, verifique os dados")

        if "cod" == "404":
            raise Exception("Cidade não encontrada, verifique as informações enviadas")

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