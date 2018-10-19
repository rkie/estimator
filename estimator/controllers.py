from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/about')
def about():
	return "About this site."