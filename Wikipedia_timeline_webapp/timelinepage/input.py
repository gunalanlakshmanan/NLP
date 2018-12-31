from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class InputForm(FlaskForm):
    articlename = StringField('Wikipedia Article Name', validators=[DataRequired(), Length(min=2, max=30)])
    timelinenumber = IntegerField('Number of Timeline sentences', validators=[DataRequired()])
    output = SubmitField('Timeline')
