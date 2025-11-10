import os
from flask import Blueprint, render_template, request, redirect, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from flask import url_for
from db import db


upload_bp = Blueprint('upload', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/', methods=['GET', 'POST'])
@login_required
def upload_paper():
    if request.method == 'POST':
        if 'paper' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['paper']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            db.papers.insert_one({
                "user_id": current_user.id,
                "filename": filename,
                "filepath": filepath,
                "status": "Pending"
            })
            flash('Paper uploaded successfully')
            return redirect(url_for('upload.upload_paper'))
        else:
            flash('File type not allowed')
    return render_template('upload.html')
