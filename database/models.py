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
	nickname = db.Column(db.String(32), nullable=False)

	def __init__(self, nickname):
		self.nickname = nickname

	def __repr__(self):
		return self.nickname
