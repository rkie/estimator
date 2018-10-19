from estimator.controllers import app

client = app.test_client()
client.testing = True

def test_index():
	response = client.get('/')
	assert response.status == '200 OK'
	html = response.get_data(as_text = True) 
	assert '<title>Agile Anonymous Estimation</title>' in html
	assert 'Let’s Estimate Something' in html

def test_index_contains_bootstrap():
	response = client.get('/')
	assert response.status == '200 OK'
	html = response.get_data(as_text = True) 
	assert 'bootstrap.min.css' in html

def test_about():
	response = client.get('/about')
	assert response.status == '200 OK'
	assert response.get_data(as_text = True) == 'About this site.'

def test_page_not_found():
	response = client.get('/not_there')
	assert response.status == '404 NOT FOUND'