import base64
import hashlib
import hmac
import os

from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

bp = Blueprint("admin_auth", __name__, template_folder="templates")


class LoginForm(FlaskForm):
    username = StringField("Usuário", validators=[DataRequired()])
    password = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")


def _decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def verify_password(password: str, stored_hash: str) -> bool:
    """Verifica uma senha armazenada com scrypt, sem guardar a senha em texto puro."""
    try:
        algorithm, n, r, p, salt_b64, hash_b64 = stored_hash.split("$")
        if algorithm != "scrypt":
            return False

        salt = _decode(salt_b64)
        expected = _decode(hash_b64)
        derived = hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=int(n),
            r=int(r),
            p=int(p),
            dklen=len(expected),
        )
        return hmac.compare_digest(derived, expected)
    except (ValueError, TypeError):
        return False


def is_admin_authenticated() -> bool:
    return session.get("admin_authenticated") is True


@bp.route("/admin/login", methods=["GET", "POST"])
def login():
    if is_admin_authenticated():
        return redirect(url_for("admin.index"))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data
        expected_username = os.getenv("ADMIN_USERNAME", "admin")
        password_hash = os.getenv("ADMIN_PASSWORD_HASH", "")

        if (
            hmac.compare_digest(username, expected_username)
            and password_hash
            and verify_password(password, password_hash)
        ):
            session.clear()
            session["admin_authenticated"] = True
            session["admin_username"] = username
            flash("Login realizado com sucesso.", "success")
            return redirect(url_for("admin.index"))

        flash("Usuário ou senha inválidos.", "danger")

    return render_template(
        "admin_login.html",
        title=current_app.config.get("TITLE", "Área administrativa"),
        form=form,
    )


@bp.route("/admin/logout")
def logout():
    session.clear()
    flash("Sessão encerrada.", "success")
    return redirect(url_for("admin_auth.login"))
