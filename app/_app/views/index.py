# -*- coding: UTF-8 -*-
import os

from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory, url_for)
from google.cloud import storage

from werkzeug.utils import secure_filename

from . import transcriber

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename: str) -> str:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


bucket_name = 'bp_yead'


def upload_blob(bucket_name, uploaded_file, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_file(uploaded_file)


@transcriber.route('/', methods=['GET'])
def index() -> str:
    """
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
    """
    return render_template('index.html', title='index')


@transcriber.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files.get('file')

    if 'file' not in request.files:
        return 'No file uploaded.', 400

    destination_blob_name = uploaded_file.filename
    upload_blob(bucket_name, uploaded_file, destination_blob_name)

    msg = 'File {} uploaded to {}.'.format(
        uploaded_file, destination_blob_name)

    return msg


@transcriber.route('/uploads/<filename>')
def uploaded_file(filename) -> str:
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
