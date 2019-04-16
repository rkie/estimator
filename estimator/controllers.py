from flask import render_template, redirect, url_for, session
from flask import Blueprint
from forms.forms import NickNameForm, NewGroupForm
from database.models import User, Group
from estimator import db

web = Blueprint('web', __name__)

@web.route('/', methods=['GET'])
def index():
	nickname = session.get('nickname')
	groups = []
	if nickname != None:
		user = User.query.filter_by(nickname=nickname)
		if user.count() > 0:
			groups = Group.query.filter_by(user=user.first().id).all()

	form = NickNameForm()
	new_group_form = NewGroupForm()
	return render_template('index.html', form=form, nickname=nickname, groups=groups, new_group_form=new_group_form)

@web.route('/', methods=['POST'])
def accept_nickname():
	form = NickNameForm()
	if form.validate_on_submit():
		session['nickname'] = form.name.data
		form.name.data = ''
	return redirect(url_for('web.index'))

@web.route('/creategroup', methods=['POST'])
def create_group():
	form = NewGroupForm()
	if form.validate_on_submit():
		nickname = session.get('nickname')
		user_query = User.query.filter_by(nickname=nickname)
		if user_query.count() == 0:
			user = User(nickname)
			db.session.add(user)
		else:
			user = user_query.first()
		group_name = form.group_name.data
		group_query = Group.query.filter_by(name=group_name, user=user.id)
		if group_query.count() > 0:
			error_message = 'That group already exists. Please try a different name.'
			back_url = url_for('web.index')
			return render_template('generic-error.html', error_message=error_message, back_url=back_url), 400
		else:
			group = Group(group_name, user)
			db.session.add(group)
	db.session.commit()
	return redirect(url_for('web.index'))

@web.route('/group/<int:id>', methods=['GET'])
def view_group(id):
	group = Group.query.get(id)
	owner = User.query.get(group.user);
	nickname = session.get('nickname')
	if owner.nickname == nickname:
		return render_template('group-owner.html', group=group)
	return render_template('group.html', group=group)

@web.route('/about')
def about():
	return "About this site."
