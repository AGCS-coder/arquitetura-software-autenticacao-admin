from flask import redirect, session, url_for
from flask_admin import Admin, AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.form import SecureForm
from flask_admin.contrib.sqla import ModelView
from flask_babel import Babel

from loja.ext.database import db
from loja.model import Product


class SecureAdminView:
    """Protege as telas do Flask-Admin com a sessão administrativa."""

    def is_accessible(self):
        return session.get("admin_authenticated") is True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("admin_auth.login"))


class SecureAdminIndexView(SecureAdminView, AdminIndexView):
    pass


class SecureModelView(SecureAdminView, ModelView):
    form_base_class = SecureForm


def init_app(app):
    Babel(app)

    # A rota de autenticação é registrada antes do Flask-Admin para que
    # /admin/login permaneça pública e a área administrativa fique protegida.
    from loja.blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    admin = Admin(
        app,
        name="Loja Architech",
        index_view=SecureAdminIndexView(),
    )
    admin.add_view(SecureModelView(Product, db.session))
    admin.add_link(MenuLink(name="Sair", endpoint="admin_auth.logout"))
