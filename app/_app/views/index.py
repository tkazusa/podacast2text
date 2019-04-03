# -*- coding: utf-8 -*-
from flask import flash, redirect, render_template, request
from google.cloud import speech, storage
from google.cloud.speech import enums, types

from . import transcriber

bucket_name = 'bp-speech'
ALLOWED_EXTENSIONS = set(['flac'])


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


def transcribe_gcs(gcs_uri: str) -> str:
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-US')

    operation = client.long_running_recognize(config, audio)

    response = operation.result()
    return response


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
    gcs_uri = 'gs:' + bucket_name + blob_filename

    msg = 'File {} uploaded.'.format(blob_filename)
    return render_template('upload.html', message=msg, gcs_uri=gcs_uri)


@transcriber.route('/transcribe', methods=['POST'])
def transcribe() -> str:
    gcs_uri = request.form['gcs_uri']
    # gcs_uri = 'gs://bp-speech/test.flac'
    flash('Starts transcription')
    response = transcribe_gcs(gcs_uri)
    flash('doing something')

    tmp = []
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        tmp.append(result.alternatives[0].transcript)

    return render_template('transcribe.html', tmp=tmp)
