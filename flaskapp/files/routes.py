import requests
from flask import Flask, render_template, redirect, request, url_for, session
from flaskapp import app
from flaskapp.files.form import *
from flaskapp.files.view import *

### Upload file page ####
@app.route("/upload_file", methods=['GET', 'POST'])
def uploadFile():
    # intiate form objects
    form = addFileForm()
    form.access_by.choices = fileForm.getClientlist()
    if form.validate_on_submit():
        form.save(
            client_id = form.access_by.data,
            file = form.uploadfile.data
        )
        return redirect(url_for('overview_files'))
    
    return render_template('files/upload_file.html', form=form)

#### File overview page ###
@app.route("/files")
def overview_files():
    return render_template(
        'files/overview_files.html',
        files = file_view.getAllFiles()
        )

### Access files page ###
@app.route("/access_files", methods=['GET', 'POST'])
def access_files():
    form = accessForm()
    form.access_by.choices = fileForm.getClientlist()
    form.access_file.choices = fileForm.getFilelist()

    if form.validate_on_submit():
        form.save(
            access_file = form.access_file.data,
            access_by = form.access_by.data
        )
        return redirect(url_for('overview_files'))
    return render_template('files/access_files.html', form=form)

### View file access page ###
@app.route("/view_file")
def view_file():
    return render_template(
        'files/view_file.html',
        access_group = file_view.getFileAccess(request.args.get('fid'))
        )