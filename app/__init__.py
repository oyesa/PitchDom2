from flask import Flask
from ..config import DevConfig
from flask_bootstrap import Bootstrap
from config import config_options
from app import views
from app.main import error


bootstrap = Bootstrap()


def create_app(config_name):

# Initializing application
  app = Flask(__name__)

# Creating the app configurations
  app.config.from_object(config_options[config_name])

# Setting up configuration
  app.config.from_object(DevConfig)
  app.config.from_pyfile('config.py')


# Initializing Flask Extensions
  bootstrap = Bootstrap(app)


# Registering the blueprint
  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  return app