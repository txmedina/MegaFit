import os
import openai
import re #regular expressions module
from markupsafe import escape #protects projects against injection attacks
from megafit import app
import sys 
sys.dont_write_bytecode = True
from flask import render_template, request, Flask, Blueprint
from .locator_form import LocatorForm

locator_blueprint = Blueprint('locator', __name__)

@locator_blueprint.route('/locator',methods=['GET', 'POST'])
@app.route('/locator',methods=['GET', 'POST'])
def locator():
  form = LocatorForm(request.form)

  if request.method == 'POST':
      if form.validate() == False:
        return render_template('locator.html', form=form)
      else:
        # The following response code adapted from example on: 
        # https://platform.openai.com/docs/guides/images/usage?context=node 
        # response = openai.Image.create(
        #  prompt=form.prompt.data,
        #  n=1,
        #  size="1024x1024"
        #)
        #display_image_url = response['data'][0]['url']

        ## May need to add code and change the render_template function call below when locator is designed
        return render_template('locator.html')
      
  elif request.method == 'GET':
      return render_template('locator.html', form=form,)