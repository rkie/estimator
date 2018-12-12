from estimator import db, create_app
from database.models import *
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

with app.app_context():
	db.create_all()
