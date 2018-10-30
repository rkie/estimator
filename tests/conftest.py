from estimator.controllers import app
import pytest

@pytest.fixture
def client():
	"Create the test client as a fixture."
	client = app.test_client()
	client.testing = True
	return client
