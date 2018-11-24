from flask import jsonify, Response, url_for
from estimator import app, db
from database.models import Group

@app.route('/rest/v1/group/<groupname>', methods = ['POST'])
def create_group(groupname):
	group = Group.query.filter_by(name=groupname).first()
	if group:
		body = { "message" : "Group already exists" }
		code = 400
		return jsonify(body), code
	else:
		print("Creating new group {}".format(groupname))
		group = Group(groupname)
		db.session.add(group)
		db.session.commit()
		body = {}
		code = 201
		return jsonify({}), code, {'location': url_for('query_group', groupname=groupname)}

@app.route('/rest/v1/group/<groupname>', methods = ['GET'])
def query_group(groupname):
	group = Group.query.filter_by(name=groupname).first()
	if group:
		return jsonify({ "groupname" : group.name })
	else:
		return Response(jsonify({ "message" : "Group not found"}), 404, mimetype='application/json')