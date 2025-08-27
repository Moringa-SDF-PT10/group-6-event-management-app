from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import config

#intialising extension
db=SQLAlchemy()
migrate=Migrate

def create_app(config_name='default'):
    app=Flask(__name__)

    app.config.from_object(config[config_name])

    db.init_app(app,db)
    migrate.init_app(app, db)
    CORS(app)

    #simply am importing models
    from app.models import event, category, associations

    from app.routes.event_routes import event_bp
    from app.routes.category_routes import category_bp
    
    app.register_blueprint(event_bp, url_prefix='/api')
    app.register_blueprint(category_bp, url_prefix='/api')
    
    return app