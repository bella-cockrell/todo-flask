from app import create_app
import pytest

@pytest.fixture
def client():
    # TODO: figure out a better way to start up the test server
    return create_app("testing")

def test_health_check(client):
    response = client.test_client().get("/health_check")
    assert response.status_code == 200