import os
import openai
import re #regular expressions module
from markupsafe import escape #protects projects against injection attacks
from megafit import app
import sys 
sys.dont_write_bytecode = True
from .create_profile_form import CreateProfileForm
from flask import render_template, request, Flask, Blueprint
from flask import flash, redirect, url_for
from megafit.database import users_collection, client
import bcrypt

create_profile_blueprint = Blueprint('create_profile', __name__)

@app.route('/create_profile',methods=['GET', 'POST'])
def create_profile():
  form = CreateProfileForm(request.form)
  
  if request.method == 'POST':     
      if form.validate() == False:
        return render_template('create_profile.html', form=form)
      else:
        username = form.username.data
        password = form.password.data 
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        firstname = form.firstname.data
        lastname = form.lastname.data
        age = form.age.data
        height = form.height.data
        email = form.email.data
        favorite_workouts = []
        
        user = users_collection.find_one({'username': username})
        if user:
          flash('Username already exists.')
          print("Username already exists")
          return render_template('create_profile.html', form=form)
        else:
          user_document = {
          "username": username,
          "first_name": firstname,
          "last_name": lastname,
          "age": age,
          "height": height,
          "email": email,
          "password": hashed_password,
          "favorite_workouts": favorite_workouts
          }

          try:
            result = users_collection.insert_one(user_document)
            flash('Profile created successfully!')
            print("You have created a profile")
            return redirect(url_for('login'))
          except Exception as e:
            print("An error occurred: ", {e})
            flash('An error occurred while creating the profile.')
            return render_template('create_profile.html', form=form)
      
  elif request.method == 'GET':
      return render_template('create_profile.html', form=form)