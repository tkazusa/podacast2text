# -*- coding: utf-8 -*-
from flask import flash, redirect, render_template, request
from google.cloud import storage

from . import transcriber

bucket_name = 'bp_yead'
ALLOWED_EXTENSIONS = set(['txt'])


def allowed_file(filename: str) -> str:
    """The allowed file names
    Args:
        filename (str): filename
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_blob(bucket_name, uploaded_file, blob_filename):
    """Uploads a file to the bucket.
    Args:
        bucket_name (str): The bucket path on GCS
        uploaded_file : file object from post request
        blob_filename (str): filename of the destination blob
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_filename)

    blob.upload_from_file(uploaded_file)


@transcriber.route('/', methods=['GET', 'POST'])
def index() -> str:
    return render_template('index.html', title='index')


@transcriber.route('/upload', methods=['POST'])
def upload() -> str:
    uploaded_file = request.files.get('file')

    if 'file' not in request.files:
        flash('No file uploaded')
        return redirect(request.url, code=302)

    if not allowed_file(uploaded_file.filename):
        flash('Forbidden file type uploaded')
        return redirect(request.url, code=302)

    blob_filename = uploaded_file.filename
    upload_blob(bucket_name, uploaded_file, blob_filename)
    gcs_uri = 'gs://bp-speech/aa.txt'

    msg = 'File {} uploaded.'.format(blob_filename)
    return render_template('upload.html', message=msg, gcs_uri=gcs_uri)


@transcriber.route('/transcribe', methods=['POST'])
def transcribe(gcs_uri) -> str:
    return render_template('transcribe.html', gcs_uri=gcs_uri)
