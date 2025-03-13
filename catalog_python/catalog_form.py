import sys 
sys.dont_write_bytecode = True
from flask_wtf import Form
from wtforms import TextAreaField, SubmitField, validators, ValidationError


class catalogForm(Form):
    prompt = TextAreaField("Please search for a workout",  [validators.InputRequired("Please enter a valid workout.")])
    submit = SubmitField("Search") 