# -*- coding: UTF-8 -*-
import os
from flask import Flask, flash, request, redirect, send_from_directory, url_for, render_template
from werkzeug.utils import secure_filename

from . import transcriber


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename: str) -> str:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@transcriber.route('/', methods=['GET', 'POST'])
def upload_file() -> str:
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('index.html', title='index')


@transcriber.route('/uploads/<filename>')
def uploaded_file(filename) -> str:
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
