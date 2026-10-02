import os
from pathlib import Path

from dotenv import load_dotenv
from dynaconf import FlaskDynaconf


def init_app(app, **config):
    # Localiza o .env na raiz do projeto
    project_root = Path(__file__).resolve().parents[2]
    env_file = project_root / ".env"
    load_dotenv(env_file)

    FlaskDynaconf(app)

    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        WTF_CSRF_ENABLED=True,
    )
