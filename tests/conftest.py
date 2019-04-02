# -*- encoding: UTF-8 -*-
import pytest

from app._app import create_app


@pytest.fixture()
def app():
    app = create_app()
    return app


@pytest.fixture()
def test_client(app):
    testing_client = app.test_client()
    return testing_client


@pytest.fixture()
def test_data():
    with open("test.flac", "w"):
        pass
