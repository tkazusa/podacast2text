# -*- encoding: UTF-8 -*-
import pytest

import app


@pytest.fixture(scope='module')
def test_client():
    testing_client = app.test_client()
    yield testing_client
