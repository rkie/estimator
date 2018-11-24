from estimator import db

class Group(db.Model):
	"""A group that team members can join and contains issues"""

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Estimation group: {}>'.format(self.name)
