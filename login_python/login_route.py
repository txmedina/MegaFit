import os
import openai
import re #regular expressions module
from markupsafe import escape #protects projects against injection attacks
from megafit import app
import sys 
sys.dont_write_bytecode = True
from .login_form import LoginForm
from flask import render_template, request, Flask, Blueprint, session
from flask import flash
from megafit.database import users_collection, client
import bcrypt

login_blueprint = Blueprint('login', __name__)

@app.route('/login',methods=['GET', 'POST'])
def login():
  form = LoginForm(request.form)
  
  if 'username' in session:
        username = session['username']
        user = users_collection.find_one({'username': username})
        return render_template('profile.html', user=user)
  
  if request.method == 'POST':
      if form.validate() == False:
        return render_template('login.html', form=form)
      else:
        username = form.username.data
        password = form.password.data.encode('utf-8')
        
        user = users_collection.find_one({'username': username})
        
        if user:
          hashed_password_bytes = user['password']
          
          if bcrypt.checkpw(password, hashed_password_bytes):
            session.clear()
            flash('Loggin successful', 'success')
            print("Login successfull")
            session['username'] = user['username']
            return render_template('home.html', form=form)
          else:
            flash('Login Unsuccessful. Username or password incorrect', 'danger')
            print('Login failed')
          
        else:
            flash('Login Unsuccessful. Username or password incorrect', 'danger')
            print("Login ailed")
            return render_template('login.html', form=form)
      
  elif request.method == 'GET':
      return render_template('login.html', form=form)