from flask import render_template, redirect, url_for, session, request
from flask import Blueprint
from forms.forms import NickNameForm, NewGroupForm
from database.models import User, Group, Membership
from estimator import db

web = Blueprint('web', __name__)

@web.route('/', methods=['GET'])
def index():
	nickname = session.get('nickname')
	groups = []
	other_groups = []
	if nickname != None:
		user = User.query.filter_by(nickname=nickname)
		if user.count() > 0:
			user_id = user.first().id
			groups = Group.query.filter_by(user=user_id).all()
			other_groups = Group.query.join(Membership).filter(Membership.user_id==user_id).all()

	form = NickNameForm()
	new_group_form = NewGroupForm()
	return render_template('index.html', form=form, nickname=nickname, groups=groups, new_group_form=new_group_form, other_groups=other_groups)

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
	id = -1
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
			db.session.flush()
			print('Flushed session to get id="{}"'.format(group.id))
			id = group.id
			membership = Membership(group, user)
			db.session.add(membership)
		db.session.commit()
		return redirect(url_for('web.view_group', id=id))
	return redirect(url_for('web.index'))

@web.route('/group/<int:id>', methods=['GET'])
def view_group(id):
	group = Group.query.get(id)
	owner = User.query.get(group.user);
	nickname = session.get('nickname')

	# make sure the user exists and is logged in
	active_user = User.query.filter_by(nickname=nickname).first()
	if active_user == None:
		return redirect(url_for('web.index'))

	# Check whether this user is a member and send to the error page if not
	membership = Membership.query.filter_by(group_id=group.id, user_id=active_user.id)

	# Look up the other members of the group to display them on the page
	members = User.query.join(Membership).filter(Membership.group_id==id).all()
	owner_in_group = len([item for item in members if item.nickname == nickname]) == 1
	print(owner_in_group)
	# return the owner or member template as appropriate
	if owner.nickname == nickname:
		join_link=url_for("web.join_group", id=id, _external=True)
		return render_template('group-owner.html', group=group, group_members=members, join_link=join_link, owner_in_group=owner_in_group)
	if membership.count() > 0:
		return render_template('group.html', group=group, group_members=members)

	# return an error if no association with the group
	error_message = 'You do not have permission to view this group.'
	back_url = url_for('web.index')
	return render_template('generic-error.html', error_message=error_message, back_url=back_url), 400

@web.route('/group/<int:id>/join', methods=['GET','POST'])
def join_group(id):
	"""Serve page to allow a user to join the group. Also accept post to join the group."""

	# show the error page if the group does not exist
	group = Group.query.get(id)
	if group == None:
		return render_template("generic-error.html", error_message='That group does not exist.')

	# ensure the user must be in the database to allow them to join
	nickname = session.get('nickname')
	active_user = User.query.filter_by(nickname=nickname).first()
	if active_user == None:
		return redirect(url_for('web.index'))

	# should not join the group more than once
	if Membership.query.filter_by(user_id=active_user.id, group_id=id).count() > 0:
		return render_template('generic-error.html', error_message='You are already in this group.')

	# serve a page that shows the group name and a form with the
	if request.method == 'GET':
		return render_template('join-group.html', group=group)

	# add the user to the group and redirect to the group page
	membership = Membership(group, active_user)
	db.session.add(membership)
	db.session.commit()
	# redirect to the group page
	return redirect(url_for('web.view_group', id=id))

@web.route('/group/<int:id>/leave', methods=['GET', 'POST'])
def leave_group(id):
	print('leaving group {}'.format(id))
	# check for existing membership
	group = Group.query.get(id)
	nickname = session.get('nickname')
	active_user = User.query.filter_by(nickname=nickname).first()
	membership = Membership.query.filter_by(group_id=id, user_id=active_user.id)
	if membership == None:
		error_message='You are not in this group.'
		return render_template('generic-error.html', error_message)
	# ask for confirmation
	if request.method == 'GET':
		return render_template('leave-group.html', group=group)
	# remove them from the group by deleting the membership row
	try:
		db.session.delete(membership.one())
		db.session.commit()
		print('session commited')
	except Exception as e:
		print(e)
		error_message='There was a problem removing you from the group.'
		return render_template('generic-error.html', error_message=error_message, back_url=url_for('web.view_group', id=id))
	return redirect(url_for('web.view_group', id=id))

@web.route('/about')
def about():
	return "About this site."
