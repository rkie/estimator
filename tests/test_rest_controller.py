from estimator.controllers import app

client = app.test_client()
client.testing = True

def test_create_group():
	# TODO: Mock the response the service returns to the controller
	response = client.post('/rest/v1/group/TestGroup')
	assert response.status == '201 Created'
    # TODO: check the content
	# TODO: verify that the group was created

def test_create_group_name_extsts():
	# TODO: Mock the response - duplicate group
	response = client.post('/rest/v1/group/TestGroup')
	assert response.status == '400 Bad request'
    # TODO: check the content
	# TODO: verify that the group was not created

def test_query_group():
	response = client.get('/rest/v1/group/TestGroup')
	assert response.status == '200 OK'
    # TODO: check the content