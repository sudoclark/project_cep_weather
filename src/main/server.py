from flask import Flask

from src.main.routes.weathers import weather_bp_routes

app = Flask(__name__)

app.register_blueprint(weather_bp_routes)