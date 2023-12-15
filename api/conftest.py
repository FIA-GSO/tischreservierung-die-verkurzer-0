import pytest
import api
import db
from api import create_app
@pytest.fixture
def testing_app():
    app = create_app()
    api.TESTING = True
    db.DATABASE = './Test-TischResDB.db'
    app.config["DEBUG"] = True
    app.config["TESTING"] = True
    return app.test_client()
