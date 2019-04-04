# -*- coding: UTF-8 -*-
from io import BytesIO

import pytest
from google.cloud import speech, storage
from google.cloud.speech import enums, types


def test_get_route(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')

    assert response.status_code == 200


def test_post_upload_with_allowed_file(test_client):
    """
    GIVEN a Flask application
    WHEN the '/upload' page is requested (POST) with allowed files
    THEN check the response is valid
    """
    response = test_client.post(
        '/upload',
        data={
            'file': (BytesIO(b'my file contents'), 'file.flac')
        }
    )

    assert response.status_code == 200


def test_post_upload_with_not_allowed_file(test_client):
    """
    GIVEN a Flask application
    WHEN the '/upload' page is requested (POST) with not allowed files
    THEN check the response is FOUND
    """
    response = test_client.post(
        '/upload',
        data={
            'file': (BytesIO(b'my file contents'), 'file.png')
        }
    )

    assert response.status_code == 302


def test_post_upload_with_no_file(test_client):
    """
    GIVEN a Flask application
    WHEN the '/upload' page is requested (POST) without files
    THEN check the response is FOUND
    """
    response = test_client.post('/upload')

    assert response.status_code == 302


@pytest.mark.skip(reason='time comsuming')
def test_post_transcribe(test_client):
    """
    GIVEN a Flask application
    WHEN the '/transcribe' page is requested (POST)
    THEN check the response is valid 
    """
    # Upload a test flac file to the GCS bucket from local dir
    bucket_name = 'bp-speech'
    blob_filepath = 'test.flac'
    local_filepath = 'dat/test.flac'

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_filepath)

    blob.upload_from_filename(filename=local_filepath)

    # test post request with .flac filepath on gcs
    gcs_uri = 'gs://' + bucket_name + '/' + blob_filepath
    response = test_client.post('/transcribe',
                                data={'gcs_uri': gcs_uri})

    assert response.status_code == 200


def test_not_found(test_client):
    """
    GIVEN a Flask application
    WHEN the '/api/not/found' page is requested (GET)
    THEN check the response is invalid
    """
    response = test_client.get('/api/not/found')

    assert response.status_code == 404
