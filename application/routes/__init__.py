from sanic import Blueprint
from .sports import bp as sport_bp
from .events import bp as event_bp

api = Blueprint.group(sport_bp, event_bp, url_prefix="/api")
