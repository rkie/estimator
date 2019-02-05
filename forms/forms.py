from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NickNameForm(FlaskForm):
    name = StringField('Please enter a nickname', validators=[DataRequired()])
    submit = SubmitField('Submit')