from flask import json, Response
from estimator import app

@app.route('/rest/v1/group/<groupname>', methods = ['POST'])
def create_group(groupname):
	# TODO: implement
	if groupname == 'NewGroup':
		body = { "message" : "Group created" }
		code = 201
	else:
		body = { "message" : "Group already exists" }
		code = 400
	return Response(json.dumps(body), status=code, mimetype='application/json')

@app.route('/rest/v1/group/<groupname>', methods = ['GET'])
def query_group(groupname):
	# TODO: implement
	if groupname == 'TestGroup':
		return json.dumps({ "groupname" : groupname })
	else:
		return Response(json.dumps({ "message" : "Group not found"}), 404, mimetype='application/json')