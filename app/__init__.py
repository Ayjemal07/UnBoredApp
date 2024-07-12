from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from dotenv import load_dotenv
import os
from app.models import db, login_manager, ma

# Load environment variables
load_dotenv()

# Initialize the database

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object('config.Config')
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from .crud_routes import crud
    from .suggestions import main
    from .authentification.auth_routes import auth

    
    app.register_blueprint(crud)
    app.register_blueprint(main)
    app.register_blueprint(auth)
    
    with app.app_context():
        # Create database tables based on models
        db.create_all()

    return app
