import json
import logging
from functools import partial

from sanic import Sanic
from sanic.worker.loader import AppLoader

from application.app import create_app

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        with open("./config/app.json", "r", encoding="UTF-8") as f:
            config = json.load(f)
    except FileNotFoundError as e:
        logger.error("Error loading config: %s", e)

    loader = AppLoader(factory=partial(create_app))
    app = loader.load()
    app.prepare(
        host=config.get("host", "0.0.0.0"),
        port=config.get("port", 8000),
        dev=config.get("dev", False),
    )
    Sanic.serve(primary=app, app_loader=loader)
