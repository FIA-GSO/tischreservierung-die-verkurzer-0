import pytest
from api import create_app


@pytest.fixture
def testing_app():
    app = create_app()
    app.config["DEBUG"] = True
    app.config["TESTING"] = True
    return app.test_client()
