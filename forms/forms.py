from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class NickNameForm(FlaskForm):
    name = StringField('Please enter a nickname', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NewGroupForm(FlaskForm):
    group_name = StringField('Enter the name of the new group', validators=[DataRequired()])
    submit = SubmitField('Create Group')

class NewIssueForm(FlaskForm):
	story_ref = StringField('Enter the story reference', validators=[DataRequired()])
	description = StringField('Enter a description of the issue:', validators=[DataRequired()])
	submit = SubmitField('Create Issue')

class EstimateForm(FlaskForm):
	estimate = IntegerField('Give a positive integer estimate', validators=[DataRequired(), NumberRange(min=0)])
	submit = SubmitField('Make Estimate')

class ReviewEstimatesForm(FlaskForm):
	submit = SubmitField('Review Estimates')
