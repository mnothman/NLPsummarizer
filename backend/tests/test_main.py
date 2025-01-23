# basic test (improve later)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_summarization_endpoint():
    response = client.post("/summarize", json={"text": "This is a test text for summarization."})
    assert response.status_code == 200
    assert "summary" in response.json()
