from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TwoStringsForm(FlaskForm):
    string1 = StringField('A string', validators=[DataRequired()])
    string2 = StringField('Another string', validators=[DataRequired()])
    submit = SubmitField('Submit')
