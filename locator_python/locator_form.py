import sys 
sys.dont_write_bytecode = True
#Need to do the following installs:
# pip install flask-wtf
# pip install email_validator
from flask_wtf import Form
from wtforms import TextAreaField, SubmitField, validators, ValidationError

class LocatorForm(Form):
    
    #Update code below for the Gym locator form
    prompt = TextAreaField("Please enter a City, State, or Zipcode",  [validators.InputRequired("Please enter a gym location.")])
    submit = SubmitField("Send") 