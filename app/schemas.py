from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class DisposalGuidance(BaseModel):
    category: str = Field(..., description="High-level category: recyclable | non-recyclable | organic | hazardous")
    category_display: str = Field(..., description="Formatted display category")
    bin_name: str = Field(..., description="Target municipal waste bin name")
    bin_color_code: str = Field(..., description="Standard visual color code for the bin (Hex)")
    bin_icon: str = Field(..., description="Visual icon identifier for bin")
    confidence: float = Field(..., description="Confidence score between 0.0 and 1.0")
    detected_item: str = Field(..., description="Identified material or waste object")
    why_paragraph: str = Field(..., description="Single-paragraph explanation of why this belongs in this bin and disposal rationale")
    preparation_tips: List[str] = Field(default_factory=list, description="Immediate preparation instructions (e.g. rinse, separate)")
    environmental_impact: str = Field(..., description="Environmental consequence of proper disposal vs misclassification")

class PredictionItem(BaseModel):
    label: str
    score: float
    category: str
    bin_name: str

class ClassifyResponse(BaseModel):
    success: bool
    inference_engine: str
    inference_time_ms: float
    primary_result: DisposalGuidance
    alternative_predictions: List[PredictionItem] = Field(default_factory=list)

class BenchmarkItemResult(BaseModel):
    file: str
    ground_truth_category: str
    ground_truth_label: str
    predicted_category: str
    predicted_label: str
    confidence: float
    category_match: bool
    label_match: bool
    latency_ms: float

class BenchmarkSummary(BaseModel):
    total_samples: int
    correct_category_count: int
    category_accuracy_pct: float
    correct_label_count: int
    label_accuracy_pct: float
    avg_latency_ms: float
    per_category_accuracy: Dict[str, Dict[str, Any]]
    details: List[BenchmarkItemResult]

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    device: str
    model_name: str
    model_loaded: bool
    avx2_present: bool
    num_threads: int
