import os
import tempfile
import pytest
from flask import Flask

from api.api import init_routes
from api.db import init_db


@pytest.fixture
def client():
    app_fixture = Flask(__name__)
    init_routes(app_fixture)
    db_fd, app_fixture.config['DATABASE'] = tempfile.mkstemp()
    app_fixture.config['TESTING'] = True

    with app_fixture.test_client() as client:
        with app_fixture.app_context():
            init_db(app_fixture)
        yield client

    os.close(db_fd)
    os.unlink(app_fixture.config['DATABASE'])
