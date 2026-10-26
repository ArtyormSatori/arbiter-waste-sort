# WasteSense AI ♻️

> **Intelligent Edge-Vision Waste Classifier & Municipal Bin Assistant**  
> *Track Submission for Arbiter Hacks V1 — Theme: "Rethinking Waste"*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![Model: ViT](https://img.shields.io/badge/Model-Vision%20Transformer%20(CPU)-blueviolet.svg)](https://huggingface.co/watersplash/waste-classification)
[![Theme: Rethinking Waste](https://img.shields.io/badge/Arbiter%20Hacks%20V1-Rethinking%20Waste-emerald.svg)](https://arbiter-hacks-v1.devpost.com/)
[![Tests: 15/15 Pass](https://img.shields.io/badge/Tests-15%2F15%20Passing-brightgreen.svg)](tests/)

---

## 1. What It Does

**WasteSense AI** is a real-time, edge-capable waste sorting assistant. When a user uploads or takes a photo of an item at the point of disposal, the app:
1. **Classifies the item** into one of four core solid waste categories:
   - 🔵 **Recyclable** (cardboard, clean paper, rigid plastics, aluminum cans, glass bottles)
   - 🟢 **Organic / Compostable** (food scraps, fruit peels, biological plant matter)
   - 🔴 **Hazardous & E-Waste** (batteries, lithium cells, chemical containers)
   - ⚫ **Non-Recyclable / Residual** (composite laminates, single-use films, contaminated trash, worn shoes/clothing)
2. **Recommends the exact municipal bin** matching international sorting standards (Blue/Yellow, Green, Red/Orange, and Grey/Black bins).
3. **Explains *WHY*** in one short, substantive paragraph—covering material physics, contamination hazards, and circular economy impacts.
4. **Delivers actionable preparation steps** (e.g., rinsing greasy food residue, separating composite lids, taping battery terminals).

---

## 2. System Architecture & Technical Execution

WasteSense AI is engineered to run anywhere—from low-power smart disposal kiosks to mobile browsers—without requiring expensive GPUs or proprietary cloud vision APIs:

```
┌────────────────────────────────────────────────────────┐
│             Web Client (Mobile / Desktop)              │
│    • Drag-and-drop Photo Upload & Camera Snapshot      │
│    • 1-Click Verified Real Sample Presets              │
│    • Interactive Bin Color Swatches & Probability Bars │
└───────────────────────────┬────────────────────────────┘
                            │ HTTP POST /api/classify
                            ▼
┌────────────────────────────────────────────────────────┐
│             FastAPI Asynchronous Gateway               │
│    • Input Validation & Image Sanitization (Pillow)    │
│    • REST Endpoints: /api/classify, /api/benchmark     │
└───────────────────────────┬────────────────────────────┘
                            │ PIL Image
                            ▼
┌────────────────────────────────────────────────────────┐
│        Real Vision Transformer Backbone (CPU)          │
│    • Model: watersplash/waste-classification (ViT)     │
│    • Zero-AVX2 optimized PyTorch CPU pipeline          │
│    • ~1.0 - 1.4s warm inference latency on edge CPU   │
└───────────────────────────┬────────────────────────────┘
                            │ Raw Softmax Distribution
                            ▼
┌────────────────────────────────────────────────────────┐
│           Municipal Rules & Guidance Engine            │
│    • 12 Fine-Grained Classes -> 4 Core Stream Mapping  │
│    • Contamination & Preparation Rule Synthesis        │
│    • Environmental Impact & Rationale Synthesis        │
└────────────────────────────────────────────────────────┘
```

- **Backbone Model**: Fine-tuned Vision Transformer (`watersplash/waste-classification`) trained across 12 granular waste classes (`battery`, `biological`, `cardboard`, `paper`, `metal`, `plastic`, `brown-glass`, `green-glass`, `white-glass`, `trash`, `clothes`, `shoes`).
- **Edge Resilience**: Operates on legacy commodity hardware (tested and verified on Intel Sandy Bridge CPU without AVX2 instructions).
- **Zero Hallucination / Mock Policy**: 100% real model inference at runtime. No stubs, mocks, or hardcoded classifications.

---

## 3. Empirical Measurement (Theme Track Requirement)

### The Specific Waste Problem Targeted: "Wishcycling" & Stream Contamination

Modern recycling programs face a systemic failure known as **"wishcycling"**—the well-intentioned but disastrous habit of tossing non-recyclable, soiled, or hazardous items into recycling bins. 

Key real-world consequences:
- **Facility Contamination**: Over 25% to 30% of incoming recycling bin loads are contaminated with unrecyclable items, causing entire truckloads to be rejected and dumped into municipal landfills or incinerators.
- **Catastrophic Facility Fires**: Discarded lithium and alkaline batteries in curbside recycling bins rupture under mechanical compaction, sparking hundreds of severe fires in waste trucks and Materials Recovery Facilities (MRFs) each year.
- **Methane Emissions**: Biodegradable food scraps trapped in anaerobic landfills degrade into methane—a greenhouse gas with 28× higher global warming potential than CO₂.

### Benchmark Evaluation on Real Waste Photography

WasteSense AI includes a curated evaluation test suite (`tests/test_dataset/`) comprising **19 real-world waste photographs** sourced from Stanford CS229 TrashNet and Wikimedia Commons.

```bash
python eval_benchmark.py
```

#### Measured Results:

| Metric | Measured Value | Notes |
|:---|:---:|:---|
| **Total Test Samples** | **19** | Real photography across all 4 target streams |
| **Category Classification Accuracy** | **84.21% (16/19)** | High-level bin assignment correctness |
| **Fine-Grained Label Accuracy** | **73.68% (14/19)** | Exact material prediction across 12 classes |
| **Hazardous Waste Recall** | **100.00% (2/2)** | Batteries accurately routed to safe drop-offs |
| **Organic Waste Recall** | **100.00% (2/2)** | Zero organic samples misdirected to landfill |
| **Recyclable Recall** | **100.00% (10/10)**| Cardboard, metal cans, glass, plastic bottles |
| **Average CPU Latency** | **1,440 ms** | Commodity dual-core CPU without AVX2 |

#### Per-Category Accuracy Breakdown:
- **Organic Waste**: `100.00%` (2/2) — Banana peel, fruit core
- **Hazardous E-Waste**: `100.00%` (2/2) — Household alkaline & NiMH batteries
- **Recyclable Stream**: `100.00%` (10/10) — PET bottles, cardboard boxes, tin cans, amber/green glass
- **Non-Recyclable Residual**: `40.00%` (2/5) — Footwear, clothing, composite film wraps

> **ML Failure Analysis Insight**: In non-recyclable plastic wraps and styrofoam, the vision backbone accurately detects plastic polymers (`plastic`), but standard municipal sorting technology requires these thin films to be treated as non-recyclable residual trash. WasteSense AI bridges this gap through its preparation guidelines and domain heuristic warnings.

### How to Measure Real-World Impact in Deployment

In an operational pilot (e.g., a university campus cafeteria, public park, or apartment complex), success would be measured using four quantitative KPIs:
1. **Curbside Contamination Rate ($\Delta CR$)**: Gravimetric audit measuring the weight percentage of non-recyclables found inside recycling bins before vs. after deployment:
   $$\Delta CR = \frac{M_{\text{contaminant, post}}}{M_{\text{total, post}}} - \frac{M_{\text{contaminant, pre}}}{M_{\text{total, pre}}}$$
   *Target: $> 40\%$ reduction in contamination within 90 days.*
2. **Hazardous Battery Divergence**: Number of batteries recovered through designated drop-off points vs. detected in general trash bales.
   *Target: Zero battery-related compaction fires.*
3. **Organic Diversion Mass**: Monthly tonnage of clean food waste diverted from landfill to municipal composting facilities.
4. **User Misclassification Rate**: User self-reporting test accuracy before vs. after using WasteSense AI guidance.

---

## 4. How to Run It

### Prerequisites
- Python 3.10, 3.11, 3.12, or 3.13
- Git

### Installation from Clean Checkout

```bash
# 1. Clone repository
git clone https://github.com/ArtyormSatori/arbiter-waste-sort.git
cd arbiter-waste-sort

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Launching the Application

Run the convenient startup script:
```bash
./run.sh
```

Or run via Uvicorn directly:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open your browser to: **`http://localhost:8000`**

### Running the Automated Test Suite

```bash
pytest -v
```
All 15 automated unit and integration tests will execute and verify model loading, disposal logic, and API contracts.

### REST API Endpoints

- `GET /`: Serves the responsive web application UI.
- `POST /api/classify`: Accepts `multipart/form-data` with an image file, executes real vision transformer inference, and returns disposal guidance.
- `GET /api/health`: Returns system health, device architecture, and model status.
- `GET /api/benchmark`: Returns dynamic evaluation results on the 19-sample test dataset.
- `GET /api/categories`: Returns supported waste categories, municipal bin schemas, and disposal rules.
- `GET /api/samples`: Lists available test sample presets for 1-click evaluation.

---

## 5. Development & Testing Details

- **Test Suite**: 15 tests covering rules mapping, classifier edge cases, and API integration.
- **Static Assets**: Self-contained vanilla CSS and JavaScript with zero external CDN runtime dependencies (except Google Fonts).
- **Mobile Compatibility**: Supports direct camera capture on smartphones using HTML5 `<input capture="environment">`.

---

## 6. License

This project is licensed under the [MIT License](LICENSE).
