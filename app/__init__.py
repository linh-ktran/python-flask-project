"""App factory and extension setup."""

import os

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app(config_name: str | None = None) -> Flask:
    """Create the Flask app with the given config (defaults to FLASK_ENV or 'development')."""
    app = Flask(__name__, instance_relative_config=True)

    config_name = config_name or os.getenv("FLASK_ENV", "development")
    app.config.from_object(f"app.config.{config_name.capitalize()}Config")

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    api = Api(app)

    from app.api.assets import blp as assets_blp
    from app.api.health import blp as health_blp
    from app.api.managers import blp as managers_blp
    from app.api.sites import blp as sites_blp

    api.register_blueprint(health_blp)
    api.register_blueprint(managers_blp)
    api.register_blueprint(sites_blp)
    api.register_blueprint(assets_blp)

    return app
