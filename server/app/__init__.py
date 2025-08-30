from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from sqlalchemy import MetaData
from app.config import config 

# Naming indexes
metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initialize extensions
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name='default'):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config[config_name]) 

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Configure CORS for React frontend
    CORS(app, origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ])

    # Token blocklist check
    from app.models.token_blocklist import TokenBlocklist
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    # Import and register blueprints
    with app.app_context():
        from app.models import Event, Category, event_categories, User, Ticket
        
        from app.routes.event_routes import event_bp
        from app.routes.category_routes import category_bp
        from app.routes.auth_routes import auth_bp
        from app.routes.user_routes import user_bp

        app.register_blueprint(event_bp, url_prefix="/api")
        app.register_blueprint(category_bp, url_prefix="/api")
        app.register_blueprint(auth_bp, url_prefix="/api")
        app.register_blueprint(user_bp, url_prefix="/api")

    return app
