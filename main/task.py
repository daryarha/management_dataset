from flask import Blueprint, flash, render_template, redirect, url_for, request, send_from_directory
from flask_login import login_required, current_user
from . import db
from .models import Dataset, Task, User
import os
from werkzeug.utils import secure_filename
from inspect import getmembers
from pprint import pprint

task = Blueprint('task', __name__)

@task.route('/task')
@login_required
def index():    
    datasets = Dataset.query.all()
    tasks = (Task.query
            .filter_by(user_id=current_user.id)
            .filter_by(is_onwork=1)
            .all()
            )
    
    # return tasks
    return render_template('task.html', name=current_user.name, my_id=current_user.id, dataset=datasets, task=tasks)#, len_task=len(task))

@task.route('/booking/<filename>')
@login_required
def booking(filename):
    dataset = Dataset.query.filter_by(link_url=filename).first()    
    tasks = (Task.query
            .filter_by(dataset_id=dataset.id)
            .filter_by(user_id=current_user.id)
            .first()
            )
    if tasks:
        dataset.is_booked = True
        tasks.is_onwork = True
        tasks.is_booked = True
        db.session.commit()
    else:
        dataset.is_booked = True
        new_task = Task(user_id=current_user.id, dataset_id=dataset.id, is_onwork=True, is_booked=True)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('task.index'))


@task.route('/delete/<filename>')
@login_required
def delete(filename):
    dataset = Dataset.query.filter_by(link_url=filename).first()    
    tasks = (Task.query
            .filter_by(dataset_id=dataset.id)
            .filter_by(user_id=current_user.id)
            .first()
            )
    if tasks:
        tasks.is_onwork = False
        db.session.commit()
    return redirect(url_for('task.index'))



@task.route('/revoke/<filename>')
@login_required
def revoke(filename):    
    dataset = Dataset.query.filter_by(link_url=filename).first()    
    tasks = (Task.query
            .filter_by(dataset_id=dataset.id)
            .filter_by(user_id=current_user.id)
            .first()
            )
    dataset.is_booked = False
    if task:
        db.session.delete(tasks)
    db.session.commit()
    return redirect(url_for('task.index'))


