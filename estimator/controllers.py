from flask import render_template
from estimator import app

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/about')
def about():
	return "About this site."