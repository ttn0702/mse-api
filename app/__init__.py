from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_cors import CORS
from config import Config

db = SQLAlchemy()


api = Api(title="Social Network API", version="1.0",
          description="API quản lý Profile, Post, và Comment")


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    app.config.from_object(Config)
    db.init_app(app)

    from app.routes import register_routes
    register_routes(api, app)

    return app
