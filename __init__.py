#__init__.py
from flask import Flask
import os

from .extentions import db
from .routes import main



def create_app():
    app = Flask(__name__)

    app.secret_key = 'chave'

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")

    db.init_app(app)

    app.register_blueprint(main)

    return app

