# CEP Weather API

API REST em Python/Flask que recebe um CEP brasileiro e retorna as condições climáticas atuais da cidade correspondente.

## O que faz

1. Recebe um CEP via POST
2. Consulta a API [ViaCEP](https://viacep.com.br/) para descobrir a cidade
3. Consulta a [OpenWeatherMap](https://openweathermap.org/) para buscar o clima atual
4. Retorna temperatura, tipo de tempo, descrição e velocidade do vento

## Estrutura

```
cep_weather_api/
├── app.py                      # Ponto de entrada da aplicação
├── src/
│   ├── main/
│   │   ├── server.py           # Configuração do Flask e registro de rotas
│   │   ├── routes/
│   │   │   └── weathers.py     # Definição do endpoint /weather_discovery
│   │   └── errors/
│   │       ├── error_handler.py        # Centraliza o tratamento de erros
│   │       ├── http_badrequest.py      # Erro 400
│   │       ├── http_not_found.py       # Erro 404
│   │       └── api_key_error.py        # Erro de autenticação
│   └── services/
│       └── get_weather.py      # Lógica principal: validação, busca de cidade e clima
└── tests/
    └── test_get_weather.py     # Testes do service
```

## Endpoint

**POST** `/weather_discovery`

Body:
```json
{ "cep": 22280070 }
```

Resposta:
```json
{
  "city": "Rio de Janeiro",
  "weather": "Clouds",
  "description": "nuvens dispersas",
  "tempeture": 22.98,
  "wind_velocity": 2.57
}
```

## Como rodar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Crie um arquivo `.env` com sua chave da OpenWeatherMap:
   ```
   API_KEY=sua_chave_aqui
   ```

3. Suba a aplicação:
   ```bash
   python app.py
   ```

4. Para rodar os testes:
   ```bash
   pytest tests/
   ```
