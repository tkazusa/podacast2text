# -*- encoding: UTF-8 -*-
def test_get_route(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    print(response.data)
    assert response.status_code == 200


def test_not_found(test_client):
    """
    GIVEN a Flask application
    WHEN the '/api/not/found' page is requested (GET)
    THEN check the response is invalid
    """
    response = test_client.get('/api/not/found')
    assert response.status_code == 404
