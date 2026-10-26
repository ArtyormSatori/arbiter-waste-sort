import os
import io
import time
from pathlib import Path
from typing import List, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import ClassifyResponse, HealthResponse, BenchmarkSummary
from app.classifier import get_classifier
from app.rules import LABEL_RULES

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"
TEST_DATASET_DIR = BASE_DIR / "tests" / "test_dataset"
BENCHMARK_FILE = BASE_DIR / "BENCHMARK_RESULTS.json"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Warm up classifier model during startup
    classifier = get_classifier()
    try:
        classifier.initialize()
    except Exception as e:
        print(f"Warning during background model warmup: {e}")
    yield

app = FastAPI(
    title="WasteSense AI - Waste Sorting Assistant",
    description="Intelligent edge-vision waste classifier and municipal bin guidance system for Arbiter Hacks V1 (Theme: Rethinking Waste)",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static web UI assets
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", response_class=HTMLResponse)
def index_page():
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        return HTMLResponse("<h3>WasteSense AI UI under construction</h3>", status_code=200)
    with open(index_file, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/health", response_model=HealthResponse)
def health_check():
    classifier = get_classifier()
    
    # Check CPU flags for AVX2
    avx2 = False
    try:
        with open("/proc/cpuinfo", "r") as f:
            avx2 = "avx2" in f.read().lower()
    except Exception:
        pass

    return HealthResponse(
        status="healthy",
        service="WasteSense AI Classification Engine",
        version="1.0.0",
        device="cpu",
        model_name=classifier.model_id,
        model_loaded=classifier.is_loaded(),
        avx2_present=avx2,
        num_threads=os.cpu_count() or 2
    )

@app.post("/api/classify", response_model=ClassifyResponse)
async def classify_waste_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a valid image format (JPEG, PNG, WebP).")
    
    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Empty image payload received.")
    if len(content) > 15 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image size exceeds 15 MB limit.")

    classifier = get_classifier()
    try:
        response = classifier.classify_image(content)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

@app.get("/api/benchmark")
def get_benchmark_results():
    if not BENCHMARK_FILE.exists():
        from eval_benchmark import run_benchmark
        summary = run_benchmark()
        return summary.model_dump()

    import json
    with open(BENCHMARK_FILE, "r") as f:
        data = json.load(f)
    return data

@app.get("/api/categories")
def get_waste_categories():
    return {
        "categories": {
            "recyclable": {
                "name": "Recyclable",
                "default_bin": "Blue / Yellow Bin",
                "description": "Clean dry cardboard, paper, rigid plastics, glass bottles, and aluminum/metal cans."
            },
            "organic": {
                "name": "Organic / Compostable",
                "default_bin": "Green Bin",
                "description": "Biodegradable food scraps, fruit peels, biological plant matter, and compostable organics."
            },
            "hazardous": {
                "name": "Hazardous & E-Waste",
                "default_bin": "Orange / Red Drop-off Depot",
                "description": "Batteries, lithium cells, chemical containers, and e-waste requiring specialized facility handling."
            },
            "non-recyclable": {
                "name": "Non-Recyclable (Landfill / Residual)",
                "default_bin": "Grey / Black Bin",
                "description": "Mixed composite packaging, heavily food-soiled paper, single-use films, and general residual solid waste."
            }
        },
        "supported_labels": list(LABEL_RULES.keys())
    }

@app.get("/api/samples")
def list_sample_images():
    manifest_path = TEST_DATASET_DIR / "manifest.json"
    if not manifest_path.exists():
        return []
    import json
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    return manifest

@app.get("/api/sample-image/{filename}")
def get_sample_image(filename: str):
    safe_name = os.path.basename(filename)
    target = TEST_DATASET_DIR / safe_name
    if not target.exists():
        raise HTTPException(status_code=404, detail="Sample image not found")
    return FileResponse(str(target), media_type="image/jpeg")
