from database.models import Group, User

def test_group_repr(default_user):
	expected = '<Estimation group: GroupName>'
	group = Group('GroupName', default_user)
	assert expected == group.__repr__()

def test_user_repr(default_user):
	expected = 'default'
	assert expected == default_user.__repr__()
