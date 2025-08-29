from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    """Application factory pattern."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configure CORS for React frontend
    CORS(app, origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ])
    
    # Import models inside app context to avoid circular imports
    with app.app_context():
        # Import models (registers them with SQLAlchemy for migrations)
        from app.models import Event, Category, event_categories
        
        # Import and register blueprints
        from app.routes.event_routes import event_bp
        from app.routes.category_routes import category_bp
        
        app.register_blueprint(event_bp, url_prefix='/api')
        app.register_blueprint(category_bp, url_prefix='/api')
    
    return app