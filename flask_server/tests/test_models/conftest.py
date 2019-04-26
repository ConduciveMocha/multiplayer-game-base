import pytest
from server.serverconfig import TestingConfig
from app import db, create_app


@pytest.fixture
def with_app():
    app = create_app(TestingConfig)
    yield app
