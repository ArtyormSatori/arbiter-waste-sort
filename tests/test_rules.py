import pytest
from app.rules import resolve_disposal_guidance, LABEL_RULES, DEFAULT_FALLBACK

def test_all_12_labels_map_to_valid_categories():
    valid_categories = {"recyclable", "non-recyclable", "organic", "hazardous"}
    for label in LABEL_RULES.keys():
        guidance = resolve_disposal_guidance(label, 0.95)
        assert guidance.category in valid_categories, f"{label} mapped to invalid category {guidance.category}"
        assert guidance.bin_name != ""
        assert guidance.bin_color_code.startswith("#")
        assert len(guidance.why_paragraph) > 50, f"Paragraph too short for {label}"
        assert len(guidance.preparation_tips) >= 1

def test_battery_is_hazardous():
    guidance = resolve_disposal_guidance("battery", 0.99)
    assert guidance.category == "hazardous"
    assert "Orange" in guidance.bin_name or "Red" in guidance.bin_name
    assert "fire" in guidance.why_paragraph.lower()

def test_biological_is_organic():
    guidance = resolve_disposal_guidance("biological", 0.98)
    assert guidance.category == "organic"
    assert "Green" in guidance.bin_name
    assert "methane" in guidance.why_paragraph.lower()

def test_cardboard_and_paper_are_recyclable():
    for lbl in ["cardboard", "paper"]:
        guidance = resolve_disposal_guidance(lbl, 0.95)
        assert guidance.category == "recyclable"
        assert "Blue" in guidance.bin_name

def test_trash_is_nonrecyclable():
    guidance = resolve_disposal_guidance("trash", 0.90)
    assert guidance.category == "non-recyclable"
    assert "Grey" in guidance.bin_name or "Black" in guidance.bin_name

def test_unknown_label_fallback():
    guidance = resolve_disposal_guidance("unknown_space_debris", 0.50)
    assert guidance.category == "non-recyclable"
    assert len(guidance.why_paragraph) > 0
