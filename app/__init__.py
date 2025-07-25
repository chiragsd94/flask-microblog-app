import os
from flask import Flask
from dotenv import load_dotenv


from app.extension import db, migrate
from app.article_routes import router


load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(router)
    return app
