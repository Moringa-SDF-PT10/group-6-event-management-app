import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from sqlalchemy import MetaData
from app.config import config

metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

#Initialize Extensions
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name='default'):
    """
    Application factory function. Configures and returns the Flask app.
    """
    #App Initialization
    app = Flask(__name__,
                static_folder='../../client/dist',
                static_url_path='/')
    app.config.from_object(config[config_name])

    #Initialize Extensions with App
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # CORS Configuration
    CORS(app, origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ])

    #Route for serving uploaded files
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    #JWT Blocklist Configuration
    from app.models.token_blocklist import TokenBlocklist
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    # Register Blueprints and Serve React App
    with app.app_context():
        from app.models import Event, Category, event_categories, User, Ticket

        # API Blueprint Registration
        from app.routes.event_routes import event_bp
        from app.routes.category_routes import category_bp
        from app.routes.auth_routes import auth_bp
        from app.routes.user_routes import user_bp
        from app.routes.ticket_routes import ticket_bp

        app.register_blueprint(event_bp, url_prefix="/api/events")
        app.register_blueprint(category_bp, url_prefix="/api/categories")
        app.register_blueprint(auth_bp, url_prefix="/api")
        app.register_blueprint(user_bp, url_prefix="/api/users")
        app.register_blueprint(ticket_bp, url_prefix="/api/tickets")

     
        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def serve(path):
            if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
                return send_from_directory(app.static_folder, path)
            else:
                return send_from_directory(app.static_folder, 'index.html')

    return app
