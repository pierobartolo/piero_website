from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class TwoStringsForm(FlaskForm):
    string1 = StringField('String1', validators=[DataRequired()])
    string2 = StringField('String2', validators=[DataRequired()])
    submit = SubmitField('Go')
