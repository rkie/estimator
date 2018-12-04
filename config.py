import os
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:

	SQLALCHEMY_TRACK_MODIFICATIONS = False

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')

class TestConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}