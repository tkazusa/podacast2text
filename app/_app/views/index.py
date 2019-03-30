# -*- coding: UTF-8 -*-
from flask import render_template, request
from google.cloud import storage

from . import transcriber

bucket_name = 'bp_yead'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


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


@transcriber.route('/', methods=['GET'])
def index() -> str:
    return render_template('index.html', title='index')


@transcriber.route('/upload', methods=['POST'])
def upload() -> str:
    uploaded_file = request.files.get('file')

    if 'file' not in request.files:
        return 'No file uploaded.', 400

    blob_filename = uploaded_file.filename
    upload_blob(bucket_name, uploaded_file, blob_filename)

    msg = 'File {} uploaded.'.format(blob_filename)

    return render_template('upload.html', message=msg)


@transcriber.route('/transcribe', methods=['POST'])
def transcribe() -> str:
    return render_template('transcribe.html')
