from flask import url_for

def test_index(client):
	response = client.get('/')
	assert response.status == '200 OK'
	html = response.get_data(as_text = True) 
	assert '<title>Agile Anonymous Estimation</title>' in html
	assert 'Let’s Estimate Something' in html

def test_index_contains_bootstrap(client):
	response = client.get('/')
	assert response.status == '200 OK'
	html = response.get_data(as_text = True) 
	assert 'bootstrap.min.css' in html

def test_about(client):
	response = client.get('/about')
	assert response.status == '200 OK'
	assert response.get_data(as_text = True) == 'About this site.'

def test_page_not_found(client):
	response = client.get('/not_there')
	assert response.status == '404 NOT FOUND'

def test_login_redirect(client, app):
	"""Ensure an attempt to reach a protected page redirecs to the login template"""
	with app.test_request_context():
		expected_url = url_for('web.login', next='/group/1', _external=True)
	response = client.get('/group/1')
	assert response.status == '302 FOUND'
	assert response.location == expected_url

def test_login_view(client):
	response = client.get('/login')
	assert response.status == '200 OK'
	assert "Enter a nickname" in response.get_data(as_text = True)

def login(client, nickname):
    return client.post('/login', data=dict(
        name=nickname
    ), follow_redirects=True)

def test_login_logout_accepted(client):
	response = login(client, 'bob')
	# will then show the option to log out on the page
	assert 'Sign Out bob' in response.get_data(as_text = True)

	response = client.get('/confirm-logout')
	# verify the message on the logout screen
	assert 'Are you sure you want to log out' in response.get_data(as_text = True)

	response = client.post('confirm-logout', follow_redirects=True)
	# the user is no longer logged in
	assert 'Sign Out bob' not in response.get_data(as_text=True)
	assert 'Click here to Login' in response.get_data(as_text=True)

def test_create_group_form(client):
	# first log in
	login(client, 'bob')
	response = client.get('/creategroup', follow_redirects=True)
	print(response.get_data(as_text=True))
	assert 'Enter the name of the new group' in response.get_data(as_text=True)

def test_create_group_post(client):
	# first log in
	login(client, 'bob')

	response = client.post('/creategroup', data=dict(group_name='Test Form'), follow_redirects=True)
	assert "Group: Test Form" in response.get_data(as_text=True)

	# try creating a duplicate group - it should fail
	response = client.post('/creategroup', data=dict(group_name='Test Form'), follow_redirects=True)
	assert "That group already exists. Please try a different name." in response.get_data(as_text=True)

def test_join_group_confirmation(client):
	login(client, 'bob')

	response = client.get('/group/1/join')
	assert 'Group: TestGroup' in response.get_data(as_text=True)
	assert 'To join the above group, click the button below.' in response.get_data(as_text=True)

def test_join_group_view_group_non_owner(client):
	login(client, 'bob')
	response = client.post('/group/1/join', follow_redirects=True)
	data = response.get_data(as_text=True)
	# check the group owner, default, and bob appear on the view group page
	assert 'default' in data
	assert 'bob' in data
	assert 'TestGroup' in data

def test_cannot_see_group_when_not_member(client):
	login(client, 'bob')
	response = client.get('/group/1')
	assert 'You do not have permission to view this group.' in response.get_data(as_text=True)

def test_join_non_existing_group(client):
	login(client, 'bob')
	response = client.get('/group/100/join')
	assert 'That group does not exist.' in response.get_data(as_text=True)

def test_cannot_join_group_twice(client):
	login(client, 'bob')
	client.post('/group/1/join', follow_redirects=True)
	response = client.post('/group/1/join', follow_redirects=True)
	assert 'You are already in this group.' in response.get_data(as_text=True)

def test_leave_group(client):
	login(client, 'bob')
	response = client.post('/group/1/join', follow_redirects=True)
	assert 'TestGroup' in response.get_data(as_text=True)
	response = client.get('/group/1/leave')
	assert 'Are you sure that you want to leave the group?' in response.get_data(as_text=True)
	response = client.post('/group/1/leave', follow_redirects=True)
	assert 'TestGroup' not in response.get_data(as_text=True)

def test_leave_group_not_in(client):
	login(client, 'bob')
	response = client.post('/group/1/leave', follow_redirects=True)
	assert 'There was a problem removing you from the group.' in response.get_data(as_text=True)

def test_create_issue(client):
	login(client, 'default')
	response = client.get('/group/1/issue')
	assert 'Create an issue:' in response.get_data(as_text=True)
	response = client.post('/group/1/issue', data=dict(
        story_ref='T-1', description='Story description'), follow_redirects=True)
	data = response.get_data(as_text=True)
	assert 'T-1' in data
	assert 'Story description' in data

def test_cannot_make_estimate_when_not_in_group(client):
	login(client, 'default')
	# leave the group
	client.post('/group/1/leave')
	# should be able to see the view
	response = client.get('/issue/1/estimate')
	assert 'You are not a voting member of this group. Please join the group to access this functionality.' in response.get_data(as_text=True)

def test_make_estimate(client):
	login(client, 'default')
	# can see the view
	response = client.get('/issue/1/estimate')
	print(response.get_data(as_text=True))
	assert 'Estimate for issue REF' in response.get_data(as_text=True)
	# make an estimate - should redirect to the group page
	response = client.post('/issue/1/estimate', follow_redirects=True, data=dict(estimate=15))
	assert 'Group: TestGroup' in response.get_data(as_text=True)

def test_view_issue_allowed(client):
	login(client, 'default')
	# can see the view
	response = client.get('/issue/1')
	assert 'Issue: REF' in response.get_data(as_text=True)

def test_view_issue__not_allowed(client):
	login(client, 'bob')
	# can see the view
	response = client.get('/issue/1')
	assert 'You are not a voting member of this group.' in response.get_data(as_text=True)

def test_review_issue_not_in_group(client):
	login(client, 'bob')
	response = client.get('/issue/1/review')
	assert 'Only thre group owner can review an issue' in response.get_data(as_text=True)

def test_review_issue_not_owner(client):
	login(client, 'bob')
	response = client.post('/group/1/join', follow_redirects=True)
	response = client.get('/issue/1/review')
	assert 'Only thre group owner can review an issue' in response.get_data(as_text=True)

def test_review_no_estimates(client):
	login(client, 'default')
	response = client.get('/issue/1/review')
	assert 'More estimates are required to provide an average.' in response.get_data(as_text=True)

def test_review_calc_average(client):
	login(client, 'bob')
	response = client.post('/group/1/join', follow_redirects=True)
	client.post('/issue/1/estimate', follow_redirects=True, data=dict(estimate=25))
	client.post('confirm-logout', follow_redirects=True)
	login(client, 'default')
	client.post('/issue/1/estimate', follow_redirects=True, data=dict(estimate=15))
	response = client.get('/issue/1/review')
	assert 'The average estimate was 20.' in response.get_data(as_text=True)

def test_lock_estimate_not_owner(client):
	login(client, 'bob')
	response = client.post('/issue/1/lock', follow_redirects=True)
	assert 'Only thre group owner can lock the estimate.' in response.get_data(as_text=True)

def test_lock_estimate(client):
	login(client, 'default')
	response = client.post('/issue/1/lock', follow_redirects=True, data=dict(estimate=13))
	assert '13' in response.get_data(as_text=True)

