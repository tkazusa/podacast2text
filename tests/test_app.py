# -*- coding: UTF-8 -*-
from io import BytesIO


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
            'file': (BytesIO(b'my file contents'), 'file.txt')
        }
    )

    assert response.status_code == 200


def test_post_upload_with_not_allowed_file(test_client):
    """
    GIVEN a Flask application
    WHEN the '/upload' page is requested (POST) with not allowed files
    THEN check the response is valid
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
    THEN check the response is BAD REQUEST
    """
    response = test_client.post('/upload')

    assert response.status_code == 302


def test_post_transcribe(test_client):
    """
    GIVEN a Flask application
    WHEN the '/transcribe' page is requested (POST)
    THEN check the response is BAD REQUEST
    """
    gcs_uri = 'test'
    response = test_client.post('/transcribe')

    assert response.status_code == 200


def test_not_found(test_client):
    """
    GIVEN a Flask application
    WHEN the '/api/not/found' page is requested (GET)
    THEN check the response is invalid
    """
    response = test_client.get('/api/not/found')

    assert response.status_code == 404
