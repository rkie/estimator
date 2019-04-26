from estimator import db

class Group(db.Model):
	"""A group that team members can join and contains issues"""
	__tablename__ = 'estimation_group'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32))
	user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __init__(self, name, user):
		self.name = name
		self.user = user.id

	def __repr__(self):
		return '<Estimation group: {}>'.format(self.name)


class User(db.Model):
	"""A user that can create groups and issues for estimation"""

	id = db.Column(db.Integer, primary_key=True)
	nickname = db.Column(db.String(32))

	def __init__(self, nickname):
		self.nickname = nickname

	def __repr__(self):
		return self.nickname

class Membership(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	group_id = db.Column(db.Integer, db.ForeignKey('estimation_group.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __init__(self, group, user):
		self.group_id = group.id
		self.user_id = user.id

class Issue(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	story_ref = db.Column(db.String(32), nullable=False)
	description = db.Column(db.String(100), nullable=False)
	group_id = db.Column(db.Integer, db.ForeignKey('estimation_group.id'), nullable=False)
	final_estimate = db.Column(db.Integer, nullable=True)

	def __init__(self, story_ref, description, group_id):
		self.story_ref = story_ref
		self.description = description
		self.group_id = group_id

	def __repr__(self):
		self.story_ref

class Estimate(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	estimate = db.Column(db.Integer)

	def __init__(self, issue_id, user_id, estimate):
		self.issue_id = issue_id
		self.user_id = user_id
		self.estimate = estimate

	def __repr__(self):
		return '{}'.format(self.estimate)
