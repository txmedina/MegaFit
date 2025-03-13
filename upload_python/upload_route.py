import os
import re
from markupsafe import escape
from megafit import app
import sys
from flask import render_template, request, Flask, Blueprint, redirect, url_for, session
from megafit.database import users_collection, db
from bson.objectid import ObjectId
from PIL import Image
import io

upload_blueprint = Blueprint('upload', __name__)

@upload_blueprint.route('/upload', methods=['GET', 'POST'])
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' in session:
        username = session['username']
        user_doc = users_collection.find_one({'username': username})
        if user_doc and 'uploads' in user_doc:
            user_uploads = user_doc['uploads']

    if request.method == 'POST':
        if 'media' in request.files:
            file = request.files['media']
            if file.filename != '':
                image = Image.open(file)
                image_bytes = io.BytesIO()
                image.save(image_bytes, format='PNG')

                user_upload = {
                    'username': username,
                    'image': image_bytes.getvalue()
                }
                db.user_upload.insert_one(user_upload)

                return redirect(url_for('upload'))

    return render_template('upload.html')