import os
import re #regular expressions module
from markupsafe import escape #protects projects against injection attacks
from megafit import app
import sys 
import requests
sys.dont_write_bytecode = True
from flask import render_template, request, Flask, Blueprint, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from megafit.database import users_collection, client

update_input_blueprint = Blueprint('update', __name__)

def convertHeight(height_ft, num_in):
      height_in = (float(num_in))/12
      float_height_ft = float(height_ft)
      height = float_height_ft + height_in
      str_height = str(height)
      return str_height

def validate_range_In(form, field):
    try:
        num = int(field.data)
        if num < 0 or num > 12:
            raise ValidationError('Value must be between 0 and 12.')
    except ValueError:
        raise ValidationError('Invalid input. Please enter a numeric value.')

def validate_range_Ft(form, field):
    try:
        num = int(field.data)
        if num < 4 or num > 7:
            raise ValidationError('Value must be between 4 and 7.')
    except ValueError:
        raise ValidationError('Invalid input. Please enter a numeric value.')


class update_form(FlaskForm):
      age = StringField('Age', validators=[DataRequired()])
      heightFt = StringField('Height', validators=[DataRequired(), validate_range_Ft])
      heightIn = StringField('Height', validators=[DataRequired(), validate_range_In])
      weight = StringField('Weight', validators=[DataRequired()])
      submit = SubmitField('Input Data')

@app.route('/update', methods=['GET', 'POST'])
def update_input():
      form = update_form(request.form)
      username = session.get('username')
      user_data = users_collection.find_one({'username': username})
      name = user_data.get('first_name')
      age = user_data.get('age')
      height = user_data.get('height')
      weight = user_data.get('weight')
      print("Username: ", username)
      if request.method == 'POST' and form.validate():
            print("Form is valid")
            height = convertHeight(form.heightFt.data, form.heightIn.data)
            user_document = {
                  "age": form.age.data,
                  "height": height,
                  "weight": form.weight.data
            }
            print("age:", form.age.data,
            "\nheight:", height,
            "\nweight:", form.weight.data)
            try:
                  result = users_collection.update_one( {'username': username}, { '$set': user_document }, upsert=True )
                  flash('Data added to profile successfully!')
                  print("Data added to profile successfully")
                  return redirect(url_for('profile'))
            except Exception as e:
                  print("An error occurred: ", {e})
                  flash('An error occurred while adding data to profile')
                  return render_template('input.html', form=form)
      elif request.method == 'GET':
            return render_template('update.html', form=form)