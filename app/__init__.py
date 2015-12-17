# Import flask and template operators
from flask import Flask, render_template


# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Implement Login Manager
from flask.ext.login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):

  # Define the WSGI application object
  web_app = Flask(__name__)

  # Configurations for web_app
  web_app.config.from_object(config[config_name])
  config[config_name].init_app(web_app)
  db.init_app(web_app)
  login_manager.init_app(web_app)

  # Sample HTTP error handling
  @web_app.errorhandler(404)
  def not_found(error):
    return render_template('404.html'), 404

  # Import a module / component using its blueprint handler variable (auth)
  # from app.main.controllers import main as main_module
  from app.main.controllers import main as main_module
  from app.auth.controllers import auth as auth_module
  from app.dashboards.controllers import dashboards as dashboard_module
  from app.settings.controllers import settings as settings_module

  # Register blueprint(s)
  web_app.register_blueprint(main_module)
  web_app.register_blueprint(auth_module)
  web_app.register_blueprint(dashboard_module)
  web_app.register_blueprint(settings_module)
  # app.register_blueprint(xyz_module)

  # Build the database:
  # This will create the database file using SQLAlchemy
  # db.create_all()

  return web_app

