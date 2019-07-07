from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Email

class LoginForm(FlaskForm):
    email = StringField('Enter your username (email address)', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class NewGroupForm(FlaskForm):
    group_name = StringField('Enter the name of the new group', validators=[DataRequired()])
    submit = SubmitField('Create Group')

class NewIssueForm(FlaskForm):
	story_ref = StringField('Enter the story reference', validators=[DataRequired()])
	description = StringField('Enter a description of the issue:', validators=[DataRequired()])
	submit = SubmitField('Create Issue')

class EstimateForm(FlaskForm):
	estimate = IntegerField('Give a positive integer estimate', validators=[DataRequired(), NumberRange(min=0, max=100)])
	submit = SubmitField('Make Estimate')

class LockEstimateForm(FlaskForm):
	estimate = IntegerField('Would you like to modify the estimate?', validators=[DataRequired(), NumberRange(min=0, max=100)])
	submit = SubmitField('Lock Estimate')
