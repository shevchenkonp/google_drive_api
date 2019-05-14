from flask import Blueprint, render_template, flash, request, current_app as app
from flask_security import login_required

from app.utils import secure_upload

from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
from googleapiclient.discovery import build

main_page = Blueprint('main_page', __name__, template_folder='templates')

@main_page.route('/', methods=['GET', 'POST'])
@main_page.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        credentials = service_account.Credentials.from_service_account_file(
            app.config['SERVICE_ACCOUNT_FILE'], scopes=app.config['SCOPES'])
        service = build('drive', 'v3', credentials=credentials)
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
