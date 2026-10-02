from flask import Blueprint
from flask_restful import Api
from .resources import ProductResource

bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)
api.add_resource(ProductResource, "/product/")

def init_app(app):
    app.register_blueprint(bp)
    print("registrou o bp")