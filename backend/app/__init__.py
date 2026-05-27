from flask import Flask
from app.api.views import api
from flask_docs import ApiDoc
from logger import logger


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api, url_prefix='/it/api')
    ApiDoc(
        app,
        title="Effekt Interface App",
        version="1.0.0",
        description="Effekt Interface app API",
    )
    app.config["API_DOC_MEMBER"] = ["api", "platform"]
    logger.info("app start-------")
    return app