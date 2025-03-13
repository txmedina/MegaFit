import os
import openai
import re #regular expressions module
from markupsafe import escape #protects projects against injection attacks
from megafit import app
import sys 
sys.dont_write_bytecode = True
from .ai_bot_form import ai_bot_form
from flask import render_template, request, Flask, Blueprint, session
from flask import flash

ai_bot_blueprint = Blueprint('ai_bot', __name__)

@app.route('/ai_bot',methods=['GET', 'POST'])
def ai_bot():
    form = ai_bot_form(request.form)
    
    
    return render_template('ai_bot.html', form=form)