from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_serializer import SerializerMixin

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

def init_app(app):
    db.init_app(app)

    from loja.model import populate_db
    with app.app_context():
        db.drop_all()
        db.create_all()
        populate_db()

