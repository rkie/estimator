from estimator import create_app, db
from database.models import Group, User, Issue, Membership
import pytest

@pytest.fixture
def app():
	"Initialize the app in test mode, initialises the DB, and adds some test cases"
	app = create_app('test')
	with app.test_request_context():
		db.create_all()
		# create a user
		user = User('default', 'default@test.com', 'password')
		db.session.add(user)
		db.session.flush()
		# create a new group
		test_group = Group('TestGroup', user)
		db.session.add(test_group)
		db.session.flush()
		# add an issue to the group
		issue = Issue('REF', 'Description', test_group.id)
		db.session.add(issue)
		# Make the user a member of the group
		membership = Membership(test_group, user)
		db.session.add(membership)
		existing_group = Group('GroupAlreadyExists', user)
		db.session.add(existing_group)
		# Second user 
		user = User('bob', 'bob@test.com', 'password')
		db.session.add(user)
		db.session.commit()
	return app

@pytest.fixture
def client(app):
	"Create the test client as a fixture."
	client = app.test_client()
	client.testing = True
	return client

@pytest.fixture
def default_user(app):
	with app.app_context():
		return User.query.filter_by(nickname='default').first()
