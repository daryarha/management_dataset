from flask import Blueprint, flash, render_template, redirect, url_for, request, send_from_directory
from flask_login import login_required, current_user
from . import db
from .models import Dataset, Task, User
import os
from werkzeug.utils import secure_filename

dataset = Blueprint('dataset', __name__)

ALLOWED_EXTENSIONS = {'zip'}

@dataset.route('/', methods=['GET', 'POST'])
@login_required
def index():        
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash('Only zip type file allowed')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            basedir = os.path.abspath(os.path.dirname(__file__))
            file.save(os.path.join(basedir, 'uploads/', filename))

            new_file = Dataset(link_url=filename, is_booked=0)
            db.session.add(new_file)
            db.session.commit()

            return redirect(url_for('task.index'))
    return render_template('dataset.html', name=current_user.name)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@dataset.route('/download/<filename>')
@login_required
def download(filename):
    return send_from_directory('./uploads/',
                               filename)


@dataset.route('/dataset/delete/<filename>')
@login_required
def delete(filename):    
    dataset = Dataset.query.filter_by(link_url=filename).first()    
    db.session.delete(dataset)
    db.session.commit()
    return redirect(url_for('task.index'))


