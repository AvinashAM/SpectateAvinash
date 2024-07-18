from sanic import Blueprint
from .sports import bp as sports_bp
from .events import bp as events_bp

api = Blueprint.group(sports_bp, events_bp, url_prefix="/api")
