from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_main_hello_world():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

