#!/usr/bin/env python3
"""
WasteSense AI - Empirical Waste Classification Benchmark Runner
Measures classification accuracy and latency on real waste photography dataset.
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, Any

from app.classifier import get_classifier
from app.schemas import BenchmarkSummary, BenchmarkItemResult

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "tests" / "test_dataset"
MANIFEST_PATH = DATASET_DIR / "manifest.json"
RESULTS_PATH = BASE_DIR / "BENCHMARK_RESULTS.json"

def run_benchmark() -> BenchmarkSummary:
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"Manifest not found at {MANIFEST_PATH}")

    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)

    classifier = get_classifier()
    print("=" * 70)
    print("WasteSense AI: Initializing Edge Vision Model Benchmark")
    print(f"Target dataset: {DATASET_DIR} ({len(manifest)} verified samples)")
    print("=" * 70)

    classifier.initialize()

    results = []
    category_stats: Dict[str, Dict[str, int]] = {}

    total_latency = 0.0
    correct_category_count = 0
    correct_label_count = 0

    for item in manifest:
        filename = item["file"]
        gt_category = item["target_category"]
        gt_label = item["ground_truth_label"]
        img_path = DATASET_DIR / filename

        if not img_path.exists():
            print(f"Skipping missing file: {filename}")
            continue

        if gt_category not in category_stats:
            category_stats[gt_category] = {"total": 0, "correct": 0}
        category_stats[gt_category]["total"] += 1

        t0 = time.perf_counter()
        with open(img_path, "rb") as f:
            resp = classifier.classify_image(f)
        lat_ms = round((time.perf_counter() - t0) * 1000.0, 2)
        total_latency += lat_ms

        pred_category = resp.primary_result.category
        pred_label = resp.alternative_predictions[0].label if resp.alternative_predictions else ""
        confidence = resp.primary_result.confidence

        cat_match = (pred_category.lower() == gt_category.lower())
        lbl_match = (pred_label.lower() == gt_label.lower())

        if cat_match:
            correct_category_count += 1
            category_stats[gt_category]["correct"] += 1
        if lbl_match:
            correct_label_count += 1

        status_mark = "✓ PASS" if cat_match else "✗ FAIL"
        print(f"[{status_mark}] {filename:<34} | GT: {gt_category:<14} -> Pred: {pred_category:<14} ({confidence:.2f}) in {lat_ms:.1f}ms")

        results.append(BenchmarkItemResult(
            file=filename,
            ground_truth_category=gt_category,
            ground_truth_label=gt_label,
            predicted_category=pred_category,
            predicted_label=pred_label,
            confidence=confidence,
            category_match=cat_match,
            label_match=lbl_match,
            latency_ms=lat_ms
        ))

    total_samples = len(results)
    cat_acc = round((correct_category_count / total_samples * 100.0), 2) if total_samples > 0 else 0.0
    lbl_acc = round((correct_label_count / total_samples * 100.0), 2) if total_samples > 0 else 0.0
    avg_lat = round((total_latency / total_samples), 2) if total_samples > 0 else 0.0

    per_cat_summary = {}
    for cat, stats in category_stats.items():
        acc = round(stats["correct"] / stats["total"] * 100.0, 2) if stats["total"] > 0 else 0.0
        per_cat_summary[cat] = {
            "total": stats["total"],
            "correct": stats["correct"],
            "accuracy_pct": acc
        }

    summary = BenchmarkSummary(
        total_samples=total_samples,
        correct_category_count=correct_category_count,
        category_accuracy_pct=cat_acc,
        correct_label_count=correct_label_count,
        label_accuracy_pct=lbl_acc,
        avg_latency_ms=avg_lat,
        per_category_accuracy=per_cat_summary,
        details=results
    )

    with open(RESULTS_PATH, "w") as f:
        json.dump(summary.model_dump(), f, indent=2)

    print("=" * 70)
    print("BENCHMARK SUMMARY RESULTS:")
    print(f"Total Test Samples evaluated : {total_samples}")
    print(f"Category Classification Acc  : {cat_acc}% ({correct_category_count}/{total_samples})")
    print(f"Fine-grained Label Acc       : {lbl_acc}% ({correct_label_count}/{total_samples})")
    print(f"Average CPU Inference Latency: {avg_lat} ms/sample")
    print("-" * 70)
    print("Per-Category Accuracy:")
    for cat, data in per_cat_summary.items():
        print(f"  - {cat:<16}: {data['accuracy_pct']:>6.2f}% ({data['correct']}/{data['total']})")
    print("=" * 70)
    print(f"Benchmark results successfully persisted to {RESULTS_PATH}")
    return summary

if __name__ == "__main__":
    run_benchmark()
