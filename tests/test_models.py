from database.models import Group

def test_repr():
	expected = '<Estimation group: GroupName>'
	group = Group('GroupName')
	assert expected == group.__repr__()
