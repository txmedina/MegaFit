import os
import openai
import re #regular expressions module
from markupsafe import escape #protects projects against injection attacks
from megafit import app
import sys 
sys.dont_write_bytecode = True
from .login_form import LoginForm
from flask import render_template, request, Flask, Blueprint, session
from flask import flash, redirect, url_for

logout_blueprint = Blueprint('logout', __name__)

@app.route('/logout',methods=['GET', 'POST'])
def logout():
    form = LoginForm(request.form)
    session.clear()
    flash('You have been logged out.', 'success')
    print('You have been logged out.')
    
    return redirect(url_for('login'))