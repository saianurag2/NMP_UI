from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from blueprint.home.views import home
from blueprint.auth.views import auth
from blueprint.device.views import device

# Globally accessible libraries
db = SQLAlchemy()
sess = Session()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    # to tie database with app
    db.init_app(app)
    # Session(app)
    sess.init_app(app)
    with app.app_context():
        db.create_all()  # Create sql tables for our data models
        # Register Blueprints
        app.register_blueprint(home)
        app.register_blueprint(auth)
        app.register_blueprint(device)
        return app


# if __name__ == "__main__":
#     create_app()
