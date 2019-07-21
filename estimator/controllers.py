from flask import render_template, redirect, url_for, request
from flask import Blueprint
from forms.forms import LoginForm, NewGroupForm, NewIssueForm, EstimateForm, LockEstimateForm, RegisterForm
from database.models import User, Group, Membership, Issue, Estimate
from estimator import db
from flask_login import login_required, login_user, logout_user, current_user
from estimator import login_manager

web = Blueprint('web', __name__)

# short, truncated Fibonacci number list
fibonacci = [1,2,3,5,8,13,21,34,55,89,100]

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@web.route('/', methods=['GET'])
def index():
	groups = []
	other_groups = []
	if current_user.is_authenticated:
		user = User.query.filter_by(nickname=current_user.nickname)
		if user.count() > 0:
			user_id = user.first().id
			groups = Group.query.filter_by(user=user_id).all()
			other_groups = Group.query.join(Membership).filter(Membership.user_id==user_id).all()
			other_groups = [item for item in other_groups if item.user != user_id]

	form = LoginForm()
	new_group_form = NewGroupForm()
	return render_template('index.html', form=form, groups=groups, new_group_form=new_group_form, other_groups=other_groups)

def find_user(email):
	user = User.query.filter_by(email=email).first()
	return user

@web.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		email = form.email.data
		# this is where real authentication should be done
		user = find_user(email)
		if user == None:
			error_message = 'Unable to log you in, please check email and password carefully.'
			return render_template('generic-error.html', error_message=error_message, back_url=url_for('web.login')), 401
		nickname = user.nickname
		if user.verify_password(form.password.data):
			login_user(user)
			next = request.args.get('next')
			if next is None or not next.startswith('/'):
				next = url_for('web.index')
			return redirect(next)
		error_message = 'Unable to log you in.'
		return render_template('generic-error.html', error_message=error_message, back_url=url_for('web.login')), 400

	return render_template('login.html', form=form)

@web.route('/creategroup', methods=['GET', 'POST'])
@login_required
def create_group():
	form = NewGroupForm()
	id = -1
	if form.validate_on_submit():
		user = current_user
		nickname = user.nickname
		user_query = User.query.filter_by(nickname=nickname)
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
			id = group.id
			membership = Membership(group, user)
			db.session.add(membership)
		db.session.commit()
		return redirect(url_for('web.view_group', id=id))
	return redirect(url_for('web.index'))

def does_group_contain(group_id, active_user_id):
	membership = Membership.query.filter_by(group_id=group_id, user_id=active_user_id)
	return membership.count() > 0

def is_group_owner(group, session_nickname):
	owner = User.query.get(group.user);
	return owner.nickname == session_nickname

@web.route('/group/<int:id>', methods=['GET'])
@login_required
def view_group(id):
	group = Group.query.get(id)
	nickname = current_user.nickname
	if nickname == None:
		error_message = 'Please log in before to taking this action.'
		return render_template('generic-error.html', error_message=error_message, back_url=url_for('web.index'))

	# make sure the user exists and is logged in
	active_user = current_user
	if active_user == None:
		return redirect(url_for('web.index'))

	# Look up the other members of the group to display them on the page
	members = User.query.join(Membership).filter(Membership.group_id==id).all()
	owner_in_group = len([item for item in members if item.nickname == nickname]) == 1

	# look up the current issues in the group
	issues = Issue.query.filter_by(group_id=id).all()

	# return the owner or member template as appropriate
	if is_group_owner(group, nickname):
		join_link = url_for("web.join_group", id=id, _external=True)
		return render_template('group-owner.html', group=group, group_members=members, join_link=join_link, owner_in_group=owner_in_group, issues=issues)
	if does_group_contain(group.id, active_user.id):
		return render_template('group.html', group=group, group_members=members, issues=issues)

	# return an error if no association with the group
	error_message = 'You do not have permission to view this group.'
	back_url = url_for('web.index')
	return render_template('generic-error.html', error_message=error_message, back_url=back_url), 400

@web.route('/group/<int:id>/join', methods=['GET','POST'])
@login_required
def join_group(id):
	"""Serve page to allow a user to join the group. Also accept post to join the group."""

	# show the error page if the group does not exist
	group = Group.query.get(id)
	if group == None:
		return render_template("generic-error.html", error_message='That group does not exist.')

	# ensure the user must be in the database to allow them to join
	nickname = current_user.nickname

	active_user = current_user
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
@login_required
def leave_group(id):
	# check for existing membership
	group = Group.query.get(id)
	active_user = current_user
	membership = Membership.query.filter_by(group_id=id, user_id=active_user.id)
	if membership == None:
		error_message='You are not in this group.'
		return render_template('generic-error.html', error_message=error_message)
	# ask for confirmation
	if request.method == 'GET':
		return render_template('leave-group.html', group=group)
	# remove them from the group by deleting the membership row
	try:
		db.session.delete(membership.one())
		# also remove any estimations in progress
		estimates = Estimate.query.filter_by(user_id=active_user.id).join(Issue).filter(Issue.group_id==id)
		[db.session.delete(item) for item in estimates.all()]
		db.session.commit()
	except Exception as e:
		error_message = 'There was a problem removing you from the group.'
		return render_template('generic-error.html', error_message=error_message, back_url=url_for('web.view_group', id=id))
	return redirect(url_for('web.index'))

@web.route('/group/<int:group_id>/issue', methods=['GET', 'POST'])
@login_required
def create_issue(group_id):
	form = NewIssueForm()
	if form.validate_on_submit():
		issue = Issue(form.story_ref.data, form.description.data, group_id)
		db.session.add(issue)
		db.session.commit()
		return redirect(url_for('web.view_group', id=group_id))
	return render_template('create-issue.html', form=form)

@web.route('/issue/<int:issue_id>/estimate', methods=['GET', 'POST'])
@login_required
def make_estimate(issue_id):
	form = EstimateForm()
	issue = Issue.query.get(issue_id)
	active_user = current_user
	# validate the user is a member
	member = Membership.query.filter_by(group_id=issue.group_id, user_id=active_user.id)
	if member.count() == 0:
		error_message = 'You are not a voting member of this group. Please join the group to access this functionality.'
		back_url = url_for('web.view_group', id=issue.group_id)
		return render_template('generic-error.html', error_message=error_message, back_url=back_url), 403

	prev_estimate = Estimate.query.filter_by(issue_id=issue_id, user_id=active_user.id).first()

	if form.validate_on_submit():
		if prev_estimate:
			prev_estimate.estimate = form.estimate.data
		else:
			estimate = Estimate(issue_id, active_user.id, form.estimate.data)
			db.session.add(estimate)
		db.session.commit()
		return redirect(url_for('web.view_group', id=issue.group_id))
	return render_template('make-estimate.html', issue=issue, form=form, prev_estimate=prev_estimate)

@web.route('/issue/<int:issue_id>')
@login_required
def view_issue(issue_id):
	[issue, members, estimates] = remaining_estimates(issue_id)
	group = Group.query.get(issue.group_id)
	is_owner = is_group_owner(group, current_user.nickname)
	member = Membership.query.filter_by(group_id=issue.group_id, user_id=current_user.id)
	if member.count() == 0:
		error_message = 'You are not a voting member of this group. Please join the group to access this functionality.'
		back_url = url_for('web.view_group', id=issue.group_id)
		return render_template('generic-error.html', error_message=error_message, back_url=back_url), 403
	return render_template('view-issue.html', issue=issue, members=members, estimates=estimates, is_owner=is_owner)

def remaining_estimates(issue_id):
	"""Returns the number of outstanding estimates for an issue"""
	issue = Issue.query.get(issue_id)
	members = Membership.query.filter_by(group_id=issue.group_id).count()
	estimates = Estimate.query.filter_by(issue_id=issue_id).count()
	return [issue, members, estimates]

@web.route('/issue/<int:issue_id>/review', methods=["GET"])
@login_required
def review_issue(issue_id):
	issue = Issue.query.get(issue_id)
	group = Group.query.get(issue.group_id)
	nickname = current_user.nickname
	if not(is_group_owner(group, nickname)):
		error_message = 'Only thre group owner can review an issue.'
		back_url = url_for('web.view_issue', issue_id=issue_id)
		return render_template('generic-error.html', error_message=error_message, back_url=back_url), 400
	try:
		average = calculate_average_estimate(issue_id)
	except ZeroDivisionError:
		error_message = 'More estimates are required to provide an average.'
		back_url = url_for('web.view_issue', issue_id=issue_id)
		return render_template('generic-error.html', error_message=error_message, back_url=back_url), 400

	# calc the nearest integer
	nearest_int = int(average)
	# calc the nearest fibonacci (up to 100)
	nearest_fib = [item for item in fibonacci if item >= nearest_int][0]

	# Create a form
	estimate_form = LockEstimateForm()
	estimate_form.estimate.default = nearest_fib
	estimate_form.process()

	# allow user to post his/her choice
	return render_template('agree-estimate.html', issue=issue, average=average, nearest_int=nearest_int, nearest_fib=nearest_fib, estimate_form=estimate_form)

def calculate_average_estimate(issue_id):
	estimates = Estimate.query.filter_by(issue_id=issue_id).all()
	total = 0
	for est in estimates:
		total += est.estimate
	average = total / len(estimates)
	return average

@web.route('/issue/<int:issue_id>/lock', methods=['POST'])
@login_required
def lock_estimate(issue_id):
	group = Group.query.join(Issue).filter(Issue.id==issue_id).first()
	nickname = current_user.nickname
	if not(is_group_owner(group, nickname)):
		error_message = 'Only thre group owner can lock the estimate.'
		back_url = url_for('web.view_issue', issue_id=issue_id)
		return render_template('generic-error.html', error_message=error_message, back_url=back_url), 400

	form = LockEstimateForm()
	if form.validate_on_submit():
		save_estimate(issue_id, form.estimate.data)
		remove_estimates(issue_id)
		issue = Issue.query.get(issue_id)
		return redirect(url_for('web.view_group', id=issue.group_id))
	return redirect(url_for('web.review_issue', issue_id=issue_id))

@web.route('/issue/<int:issue_id>/startover', methods=['GET', 'POST'])
@login_required
def start_over(issue_id):
	issue = Issue.query.get(issue_id)
	group = Group.query.get(issue.group_id)
	nickname = current_user.nickname
	if not(is_group_owner(group, nickname)):
		error_message = 'Only thre group owner can restart estimation.'
		back_url = url_for('web.view_issue', issue_id=issue_id)
		return render_template('generic-error.html', error_message=error_message, back_url=back_url), 400

	if request.method == 'GET':
		return render_template('confirm-start-over.html', issue=issue)
	remove_estimates(issue_id)
	return redirect(url_for('web.view_group', id=issue.group_id))

def save_estimate(issue_id, estimate):
	issue = Issue.query.get(issue_id)
	issue.final_estimate = estimate
	db.session.commit()

def remove_estimates(issue_id):
	estimates = Estimate.query.filter_by(issue_id=issue_id)
	estimates.delete()
	db.session.commit()

@web.route('/confirm-logout', methods=['GET', 'POST'])
@login_required
def confirm_logout():
	if request.method == 'GET':
		return render_template('confirm-logout.html')
	logout_user()
	return redirect(url_for('web.index'))

@web.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if request.method == 'GET':
		return render_template('register.html', form=form)
	if form.validate_on_submit():
		# check user not already registered
		user = User.query.filter_by(email=form.email.data)
		if user.count() > 0:
			error_message = 'This email address has already been registered.'
			back_url = url_for('web.register')
			return render_template('generic-error.html', error_message=error_message, back_url=back_url), 400
		# add the new user
		user = User(form.nickname.data, form.email.data, form.password.data)
		db.session.add(user)
		db.session.commit()
		# log them in
		login_user(user)
		# redirect to home
		return redirect(url_for('web.index'))
	# return just the basic view
	return render_template('register.html', form=form)

@web.app_errorhandler(404)
def wrong_page(err):
	error_message = 'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again. Apologies for this inconvenience.'
	return render_template('generic-error.html', error_message=error_message), 404

@web.route('/about')
def about():
	return "About this site."
