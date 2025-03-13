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

calorie_blueprint = Blueprint('calorie', __name__)
calc_blueprint = Blueprint('calorie/calculator', __name__)
input_blueprint = Blueprint('calorie/input', __name__)
metrics_blueprint = Blueprint('calorie/metrics', __name__)

navigation_links = [{'title': 'Tracker', 'url': '/calorie'},
                    {'title': 'input', 'url': '/calorie/input'},
                    {'title': 'calculator', 'url': '/calorie/calculator'},
                    {'title': 'metrics', 'url': '/calorie/metrics'}]

@calorie_blueprint.route('/calorie',methods=['GET', 'POST'])
@app.route('/calorie',methods=['GET', 'POST'])
def calorie():
      if 'username' in session:
            username = session.get('username')
            user_data = users_collection.find_one({'username': username})
            
            print("User: ", username, " in session")
            age = user_data.get('age')
            height = user_data.get('height')
            weight = user_data.get('weight')
            print("Age: ", age, "\nHeight: ", height, "\nWeight: ", weight)
            return render_template('calorie.html')
      else:
            print("No userID in Session")
            return render_template('calorie_redirect.html')

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
    
##Data Input Routes/Forms##
class input_form(FlaskForm):
      age = StringField('Age', validators=[DataRequired()])
      heightFt = StringField('Height', validators=[DataRequired(), validate_range_Ft])
      heightIn = StringField('Height', validators=[DataRequired(), validate_range_In])
      weight = StringField('Weight', validators=[DataRequired()])
      submit = SubmitField('Input Data')
@app.route('/calorie/input', methods=['GET','POST'])
def input():
      form = input_form(request.form)
      username = session.get('username')
      user_data = users_collection.find_one({'username': username})
      name = user_data.get('first_name')
      age = user_data.get('age')
      height = user_data.get('height')
      weight = user_data.get('weight')
      if age != None and height != None and weight != None:
            if request.method == 'POST' and form.validate():
                  print("Age: ", age, "\nHeight: ", height, "\nWeight: ", weight)
                  return render_template('input.html', navigation_links=navigation_links,form=form,name=name)
            elif request.method == 'GET':
                  print("Age: ", age, "\nHeight: ", height, "\nWeight: ", weight)
                  return render_template('input.html', navigation_links=navigation_links, form=form,name=name)
      else: 
            if request.method == 'POST' and form.validate():
                  username = session.get('username')
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
                        return redirect(url_for('calorie'))
                  except Exception as e:
                        print("An error occurred: ", {e})
                        flash('An error occurred while adding data to profile')
                        return render_template('new_input.html', navigation_links=navigation_links, form=form)
            elif request.method == 'GET':
                  return render_template('new_input.html', navigation_links=navigation_links, form=form)
            
'''@app.route('/calorie/new_input', methods=['GET', 'POST'])
def new_input():
      form = input_form(request.form)
      username = session.get('username')
      user_data = users_collection.find_one({'username': username})
      name = user_data.get('first_name')
      age = user_data.get('age')
      height = user_data.get('height')
      weight = user_data.get('weight')
      print("Username: ", username)
      if request.method == 'POST' and form.validate():
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
                  return redirect(url_for('calorie'))
            except Exception as e:
                  print("An error occurred: ", {e})
                  flash('An error occurred while adding data to profile')
                  return render_template('new_input.html', navigation_links=navigation_links, form=form)
      elif request.method == 'GET':
            return render_template('new_input.html', navigation_links=navigation_links, form=form)'''

def toCM(height_feet):
      height_cm = round(float(height_feet) * 30.48, 2)
      return str(height_cm)

def toKG(weight_lb):
      weight_kg = round(float(weight_lb) * 0.45359237, 2)
      return str(weight_kg)



##Calculators Routes/Forms##
class calculator_form(FlaskForm):
      weight = StringField('Weight', validators=[DataRequired()])
      submit = SubmitField('Calculate BMI')
@app.route('/calorie/calculator',methods=['GET', 'POST'])
def calculator():
      form = calculator_form(request.form)
      username = session.get('username')
      user_data = users_collection.find_one({'username': username})
      age = user_data.get('age')
      height = user_data.get('height')
      if age != None and height != None:
            if request.method == 'POST' and form.validate(): 
                  weight = form.weight.data
                  url = "https://fitness-calculator.p.rapidapi.com/bmi"
                  heightCM = toCM(height)
                  weightKG = toKG(weight)
                  querystring = {"age":age,"weight":weightKG,"height":heightCM}
                  headers = {
                        "X-RapidAPI-Key": "247584d5a9msh833da7d91332161p10fc54jsn445927f61879",
                        "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com"
                  }                 
                  response = requests.get(url, headers=headers, params=querystring)
                  print(response.json())
                  data = response.json().get('data')
                  BMI = data.get('bmi')
                  health = data.get('health')
                  print('Age: ', age, 'years\nHeight: ', height, 'ft.\nWeight: ', weight, 'lbs.\nHealth:', health, '\nBMI: ', BMI)
                  return render_template('calculator_output.html',navigation_links=navigation_links, BMI=BMI, health=health, age=age, weight=weight,height=height)
            elif request.method == "GET":
                  return render_template('calculator.html',form=form,navigation_links=navigation_links)

      else:
            return render_template('calculator_redirect.html',form=form, navigation_links=navigation_links)




##Metrics Routes##
@app.route('/calorie/metrics')
def metrics():
      return render_template('metrics.html', navigation_links=navigation_links)