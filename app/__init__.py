from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from config import Config

db = SQLAlchemy()

# Tạo đối tượng API từ Flask-RESTx
api = Api(title="Social Network API", version="1.0", description="API quản lý User, Post, và Comment")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # Đăng ký API
    from app.routes import register_routes
    register_routes(api, app)

    return app
