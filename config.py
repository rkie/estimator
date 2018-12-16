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
	DB_USERNAME = os.getenv('ESTIMATOR_USER')
	DB_PASSWORD = os.getenv('ESTIMATOR_PASSWORD')
	DB_HOST = os.getenv('ESTIMATOR_DB_HOST')
	DATABASE_NAME = os.getenv('ESTIMATOR_DATABASE')
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s/%s' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DATABASE_NAME)

config = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}