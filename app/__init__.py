# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Implement Login Manager
from flask.ext.login import LoginManager, login_required
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):

  # Define the WSGI application object
  app = Flask(__name__)

  # Configurations
  app.config.from_object(config[config_name])  # ('config')
  config[config_name].init_app(app)
  db.init_app(app)
  login_manager.init_app(app)

  # Sample HTTP error handling
  @app.errorhandler(404)
  def not_found(error):
    return render_template('404.html'), 404

  @app.route('/index')
  @login_required
  def index():
    return render_template('index.html')

  @app.route('/assets')
  @login_required
  def assets():
    return render_template('assets.html')

  # Import a module / component using its blueprint handler variable (auth)
  # from app.main.controllers import main as main_module
  from app.main.controllers import main as main_module
  from app.auth.controllers import auth as auth_module

  # Register blueprint(s)
  app.register_blueprint(main_module)
  app.register_blueprint(auth_module)
  # app.register_blueprint(xyz_module)

  # Build the database:
  # This will create the database file using SQLAlchemy
  # db.create_all()
  return app

