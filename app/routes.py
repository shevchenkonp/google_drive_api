# -*- coding: utf-8 -*-
import os
from googleapiclient.http import MediaFileUpload
from app import app, db, service
from app.models import User, Role
from werkzeug.utils import secure_filename
from flask import render_template, flash, request
from flask_security import login_required


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def secure_upload(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return True
    else:
        flash('PROHIBITED FORMAT!')
        return False


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        file = request.files['file']
        if secure_upload(file):
            file_metadata = {'name': file.filename,
                             'parents': [app.config['FOLDER_ID']]}
            file_path = app.config['FILE_PATH'].format(file.filename)
            media = MediaFileUpload(file_path, resumable=True)
            upload_file = service.files().create(body=file_metadata,
                                                 media_body=media,
                                                 fields='id').execute()
            flash('The file was uploaded!')
    return render_template('index.html')
