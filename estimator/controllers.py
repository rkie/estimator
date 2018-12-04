from flask import render_template
from flask import Blueprint

web = Blueprint('web', __name__)

@web.route('/')
def hello():
	return render_template('index.html')

@web.route('/about')
def about():
	return "About this site."