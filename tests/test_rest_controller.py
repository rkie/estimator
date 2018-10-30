
def test_create_group(client):
	# TODO: Mock the response the service returns to the controller
	response = client.post('/rest/v1/group/NewGroup')
	assert response.status == '201 CREATED'
    # TODO: check the content
	# TODO: verify that the group was created

def test_create_group_name_extsts(client):
	# TODO: Mock the response - duplicate group
	response = client.post('/rest/v1/group/GroupAlreadyExists')
	assert response.status == '400 BAD REQUEST'
    # TODO: check the content
	# TODO: verify that the group was not created

def test_query_group(client):
	response = client.get('/rest/v1/group/TestGroup')
	assert response.status == '200 OK'
    # TODO: check the content

def test_query_group_not_found(client):
	response = client.get('/rest/v1/group/UnknownGroup')
	assert response.status == '404 NOT FOUND'
    # TODO: check the content