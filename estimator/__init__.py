from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'web.login'

def create_app(config_name):
	app = Flask(__name__)
	# load the appropriate config
	app.config.from_object(config[config_name])

	config[config_name].init_app(app)
	bootstrap.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)

	from .controllers import web as web_blueprint
	app.register_blueprint(web_blueprint)

	from .rest_controller import api as api_blueprint
	app.register_blueprint(api_blueprint)

	return app
