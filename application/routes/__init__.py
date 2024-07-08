from sanic import Blueprint
from .sport import bp as sport_bp

api = Blueprint.group(sport_bp, url_prefix="/api")
