from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class ai_bot_form(FlaskForm):
    userInput = StringField('input', validators=[DataRequired()])
    ai_output = PasswordField('ai_output', validators=[DataRequired()])


    