from flask import Flask
from flask_bootstrap import Bootstrap
from config import config_options
from flask_sqlalchemy import SQLAlchemy



bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):

    app = Flask(__name__)

    # Setting up configuration
    app.config.from_object(config_options[config_name])

    # Initializing Flask Extensions
    bootstrap.init_app(app)
    db.init_app(app)
    # login_manager.init_app(app)
    # mail.init_app(app)

    # configure UploadSet
    # configure_uploads(app,photos)

    # Registering the blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/authenticate')

    return app
