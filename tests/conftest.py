from estimator import create_app, db
from database.models import Group
import pytest

@pytest.fixture
def app():
	"Initialize the app in test mode, initialises the DB, and adds some test cases"
	app = create_app('test')
	with app.app_context():
		db.create_all()
		test_group = Group('TestGroup')
		db.session.add(test_group)
		existing_group = Group('GroupAlreadyExists')
		db.session.add(existing_group)
		db.session.commit()
	return app

@pytest.fixture
def client(app):
	"Create the test client as a fixture."
	client = app.test_client()
	client.testing = True
	return client
