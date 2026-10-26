import pytest
import io
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_index_page():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "WasteSense AI" in resp.text

def test_health_check():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert "watersplash/waste-classification" in data["model_name"]

def test_categories_endpoint():
    resp = client.get("/api/categories")
    assert resp.status_code == 200
    data = resp.json()
    assert "recyclable" in data["categories"]
    assert "organic" in data["categories"]
    assert "hazardous" in data["categories"]
    assert "non-recyclable" in data["categories"]

def test_classify_valid_image():
    # Create small test in-memory image
    img = Image.new("RGB", (100, 100), color=(30, 200, 50))
    bio = io.BytesIO()
    img.save(bio, format="JPEG")
    bio.seek(0)

    files = {"file": ("test.jpg", bio, "image/jpeg")}
    resp = client.post("/api/classify", files=files)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "primary_result" in data
    assert data["primary_result"]["category"] in ["recyclable", "non-recyclable", "organic", "hazardous"]

def test_classify_invalid_file_type():
    files = {"file": ("test.txt", io.BytesIO(b"not an image"), "text/plain")}
    resp = client.post("/api/classify", files=files)
    assert resp.status_code == 400
    assert "valid image" in resp.json()["detail"].lower()

def test_benchmark_endpoint():
    resp = client.get("/api/benchmark")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_samples"] >= 15
    assert data["category_accuracy_pct"] > 70.0
