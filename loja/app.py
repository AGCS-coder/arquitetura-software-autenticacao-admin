from flask import Flask
from loja.ext import database, admin, appearance, configuration
from loja.blueprints import webui, restapi


def create_app(**config):
    app = Flask(__name__, template_folder="templates")
    configuration.init_app(app, **config)
    database.init_app(app)
    appearance.init_app(app)
    admin.init_app(app)
    webui.init_app(app)
    restapi.init_app(app)

    return app
