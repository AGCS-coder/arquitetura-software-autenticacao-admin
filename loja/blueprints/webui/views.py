from loja.ext.database import db
from loja.model import Product
from flask import render_template

def index():
    products = db.session.execute(
        db.select(Product).order_by(Product.description)).scalars()

    return render_template("products.html", products=products)

def product(product_id):
    product = db.session.execute(
        db.select(Product).filter_by(id=product_id)).scalar()

    return render_template("product.html", product=product)


