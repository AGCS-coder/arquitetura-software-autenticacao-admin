from flask import jsonify, abort
from flask_restful import Resource
from loja.model import Product

class ProductResource(Resource):
    def get(self):
        print("ProductResource")
        products = Product.query.all() or abort(204)
        return jsonify(
            {'products':[
                {
                    'id':product.id,
                    'description':product.description,
                    'price':product.price,
                }
                for product in products
            ]}
        )