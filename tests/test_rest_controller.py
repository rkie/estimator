from estimator import db
from database.models import Group

# Initialize the in-memory DB and add some entities required for testing
db.create_all()
test_group = Group('TestGroup')
db.session.add(test_group)
existing_group = Group('GroupAlreadyExists')
db.session.add(existing_group)
db.session.commit()

# clear out any existing groups
to_delete = Group.query.filter_by(name='NewGroup')
[db.session.delete(item) for item in to_delete]
db.session.commit()


def test_create_group(client):
	response = client.post('/rest/v1/group/NewGroup')
	assert response.status == '201 CREATED'
	assert response.get_data() == b'{}\n'
	assert response.headers['Location'] == 'http://localhost/rest/v1/group/NewGroup'
	assert response.headers['Content-Type'] == 'application/json'
	# Verify there is a row in the database
	g = Group.query.filter_by(name='NewGroup').first()
	assert g

def test_create_group_name_extsts(client):
	response = client.post('/rest/v1/group/GroupAlreadyExists')
	assert response.status == '400 BAD REQUEST'
	assert response.headers['Content-Type'] == 'application/json'
    # TODO: check the content
	# TODO: verify that the group was not created

def test_query_group(client):
	response = client.get('/rest/v1/group/TestGroup')
	assert response.status == '200 OK'
	assert response.headers['Content-Type'] == 'application/json'
    # TODO: check the content

def test_query_group_not_found(client):
	response = client.get('/rest/v1/group/UnknownGroup')
	assert response.status == '404 NOT FOUND'
	assert response.headers['Content-Type'] == 'application/json'