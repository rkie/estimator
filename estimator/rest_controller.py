from flask import json
from estimator import app

@app.route('/rest/v1/group/<groupname>', methods = ['POST'])
def create_group(groupname):
	return 'Group created'

@app.route('/rest/v1/group/<groupname>', methods = ['GET'])
def query_group(groupname):
	return '{ "groupname" : "' + groupname + '" }'