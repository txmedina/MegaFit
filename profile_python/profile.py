import os
import openai
import re #regular expressions module
from markupsafe import escape #protects projects against injection attacks
from megafit import app
import sys 
sys.dont_write_bytecode = True
from flask import render_template, request, Flask, Blueprint
from flask import render_template, session, redirect, url_for
from megafit.database import users_collection

profile_blueprint = Blueprint('profile', __name__)

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))  
    
    username = session['username']
    user = users_collection.find_one({'username': username})
    if not user:
        return "User not found", 404  
    
    return render_template('profile.html', user=user)