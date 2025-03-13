import os
import openai
import re #regular expressions module
from markupsafe import escape #protects projects against injection attacks
from megafit import app
import sys 
sys.dont_write_bytecode = True
from flask import render_template, request, Flask,Blueprint, session
from flask_mail import Message, Mail

from .locator_python.locator_route import locator_blueprint
from .catalog_python.catalog_route import catalog_blueprint
from .login_python.login_route import login_blueprint
from .calorie_python.calorie_route import calorie_blueprint, calc_blueprint, input_blueprint, metrics_blueprint
from.calorie_python.update_route import update_input_blueprint
from .create_profile_python.create_profile_route import create_profile_blueprint
from .upload_python.upload_route import upload_blueprint
from .login_python.logout_route import logout_blueprint
from .ai_bot_python.ai_bot_route import ai_bot_blueprint
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from megafit.database import users_collection, client

#The mail_user_name and mail_app_password values are in the .env file
#Google requires an App Password as of May, 2022: 
#https://support.google.com/accounts/answer/6010255?hl=en&visit_id=637896899107643254-869975220&p=less-secure-apps&rd=1#zippy=%2Cuse-an-app-password

mail_user_name = os.getenv('GMAIL_USER_NAME')
mail_app_password = os.getenv('GMAIL_APP_PASSWORD')
openai.api_key = os.getenv('OPENAI_API_KEY')

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = mail_user_name
app.config['MAIL_PASSWORD'] = mail_app_password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# This is the home page that the user sees when they first visit the website
@app.route('/')
def home():
  try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!") 
  except Exception as e:
    print(e)
  
  return render_template('home.html')


# This renders the error page when the user enters/visits a page that does not exist
@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404


app.register_blueprint(locator_blueprint) 
app.register_blueprint(catalog_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(calorie_blueprint)
app.register_blueprint(create_profile_blueprint)
app.register_blueprint(upload_blueprint)
app.register_blueprint(logout_blueprint)
app.register_blueprint(calc_blueprint)
app.register_blueprint(metrics_blueprint)
app.register_blueprint(input_blueprint)
app.register_blueprint(ai_bot_blueprint)
app.register_blueprint(update_input_blueprint)

