from flask import render_template, redirect, url_for, session
from flask import Blueprint
from forms.forms import NickNameForm

web = Blueprint('web', __name__)

@web.route('/', methods=['GET'])
def index():
	form = NickNameForm()
	return render_template('index.html', form=form, nickname=session.get('nickname'))

@web.route('/', methods=['POST'])
def accept_nickname():
	form = NickNameForm()
	if form.validate_on_submit():
		session['nickname'] = form.name.data
		form.name.data = ''
	return redirect(url_for('web.index'))

@web.route('/about')
def about():
	return "About this site."
