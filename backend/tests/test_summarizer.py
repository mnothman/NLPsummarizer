import sys
import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.summarizer import summarize_text

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.summarizer import summarize_text

client = TestClient(app)

# backend test, test the async API
def test_summarize_text():
    """Test if summarization function returns a string"""
    text = "This is a test input to summarize."
    summary = summarize_text(text)
    assert isinstance(summary, str)
    assert len(summary) > 0

def test_api_summarization():
    """Test API endpoint with valid input"""
    response = client.post("/summarize", json={"text": "This is a test sentence."})
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert isinstance(data["summary"], str)

def test_api_empty_input():
    """Test API with empty input"""
    response = client.post("/summarize", json={"text": ""})
    assert response.status_code == 400
    assert response.json()["error"] == "Input text cannot be empty."

def test_api_invalid_json():
    """Test API with invalid JSON format"""
    response = client.post("/summarize", content="invalid json")  # Use content instead of data (avoid test error)
    assert response.status_code == 400
    assert response.json()["error"] == "Invalid JSON format in request body."
