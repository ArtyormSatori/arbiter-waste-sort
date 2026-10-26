import pytest
from pathlib import Path
from PIL import Image
from app.classifier import get_classifier

BASE_DIR = Path(__file__).resolve().parent.parent

def test_classifier_initialization():
    clf = get_classifier()
    clf.initialize()
    assert clf.is_loaded() is True

def test_classifier_real_inference_synthetic():
    clf = get_classifier()
    img = Image.new("RGB", (224, 224), color=(80, 120, 200))
    resp = clf.classify_image(img)
    assert resp.success is True
    assert resp.inference_time_ms > 0
    assert resp.primary_result.category in {"recyclable", "non-recyclable", "organic", "hazardous"}
    assert len(resp.alternative_predictions) > 0

def test_classifier_real_dataset_sample():
    clf = get_classifier()
    sample_path = BASE_DIR / "tests" / "test_dataset" / "organic_banana_peel.jpg"
    assert sample_path.exists(), "Sample test image not found"
    
    with open(sample_path, "rb") as f:
        resp = clf.classify_image(f)
    
    assert resp.success is True
    assert resp.primary_result.category == "organic"
    assert resp.primary_result.bin_name.startswith("Green")
