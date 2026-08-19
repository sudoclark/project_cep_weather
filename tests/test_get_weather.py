import pytest
from pytest import raises
from src.services.get_weather import GetWeather

class MockRequest:
    def __init__(self, body):
        self.json = body

def test_get_weather():
    """
    Teste de integração. Teste do fluxo inteiro da aplicação, valida se o body está correto, valida as chamadas
    às APIs e valida a formatação dos dados.
    """
    mock_request = MockRequest({"cep": 22280070})
    get_weather_service = GetWeather()

    response = get_weather_service.get_weather(mock_request)

    assert response == {'city': 'Rio de Janeiro', 'weather': 'Clouds', 'description': 'nuvens dispersas', 'tempeture': 22.98, 'wind_velocity': 2.57}

def test_get_weather_incorrect_cep_field_error():
    """
    Teste que valida se o campo 'cep' está informado corretamente no body. Valida, principalmente,
    o método interno de validação de dados do service.
    """
    mock_request = MockRequest({"cep_number": 22280070})
    get_weather_service = GetWeather()

    with raises(Exception) as exc_info:
        get_weather_service.get_weather(mock_request)

    assert str(exc_info.value) == "Dados incorretos, verifique os campos enviados."

def test_space_in_cep_error():
    """
    Teste que valida um valor incorreto para o campo 'cep'. Aqui validamos a Exception que verifica se o valor
    contém algum espaçamento incluso.
    """
    mock_request = MockRequest({"cep": "222 0070"})
    get_weather_service = GetWeather()

    with raises(Exception) as exc_info:
        get_weather_service.get_weather(mock_request)

    assert str(exc_info.value) == "O cep não deve conter espaços."

def test_cep_not_str_instance_error():
    """
    Teste que valida se o 'cep' é do tipo int() corretamente. Valida a Exception que verifica se o usuário não
    enviou o tipo de dado incorreto.
    """
    mock_request = MockRequest({"cep": "22280070"})
    get_weather_service = GetWeather()

    with raises(Exception) as exc_info:
        get_weather_service.get_weather(mock_request)

    assert str(exc_info.value) == "O cep fornecido deve ser um número."