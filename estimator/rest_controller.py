from flask import Response
from estimator import app

@app.route('/rest/v1/group/<groupname>', methods = ['POST'])
def create_group(groupname):
	# TODO: implement
	if groupname == 'NewGroup':
		body = '{ "message" : "Group created" }'
		code = 201
	else:
		body = '{ "message" : "Group exists" }'
		code = 400
	return Response(body, status=code, mimetype='application/json')

@app.route('/rest/v1/group/<groupname>', methods = ['GET'])
def query_group(groupname):
	return '{ "groupname" : "' + groupname + '" }'