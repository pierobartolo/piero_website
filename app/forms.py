from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TwoStringsForm(FlaskForm):
    string1 = StringField('', validators=[DataRequired()])
    string2 = StringField('', validators=[DataRequired()])
    submit = SubmitField('Submit')
