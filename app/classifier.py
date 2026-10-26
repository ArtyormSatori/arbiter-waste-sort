import os
import time
import io
import logging
from typing import List, Dict, Any, Tuple, Optional
from PIL import Image

from app.schemas import ClassifyResponse, PredictionItem
from app.rules import resolve_disposal_guidance, map_predictions

logger = logging.getLogger("wastesense.classifier")

MODEL_ID = "watersplash/waste-classification"

class WasteClassifier:
    _instance: Optional["WasteClassifier"] = None

    def __init__(self, model_id: str = MODEL_ID):
        self.model_id = model_id
        self._pipeline = None
        self._initialized = False

    @classmethod
    def get_instance(cls) -> "WasteClassifier":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def initialize(self):
        if self._initialized and self._pipeline is not None:
            return

        import torch
        from transformers import pipeline

        # Configure CPU thread count for responsive throughput on commodity host
        num_cores = os.cpu_count() or 2
        torch.set_num_threads(max(1, min(4, num_cores)))

        logger.info(f"Loading local Vision Transformer: {self.model_id} (CPU threads: {torch.get_num_threads()})")
        t0 = time.time()
        self._pipeline = pipeline(
            "image-classification",
            model=self.model_id,
            device="cpu"
        )
        self._initialized = True
        logger.info(f"Model loaded successfully in {time.time() - t0:.2f}s")

    def is_loaded(self) -> bool:
        return self._initialized and self._pipeline is not None

    def classify_image(self, image_input: Any) -> ClassifyResponse:
        """
        Accepts PIL Image, bytes, or file-like object.
        Executes real inference and formats result.
        """
        if not self.is_loaded():
            self.initialize()

        # Parse and sanitize image
        pil_img = self._to_pil_image(image_input)

        t0 = time.perf_counter()
        raw_preds = self._pipeline(pil_img, top_k=5)
        latency_ms = round((time.perf_counter() - t0) * 1000.0, 2)

        if not raw_preds:
            raise ValueError("Model returned empty prediction set")

        top_pred = raw_preds[0]
        top_label = top_pred.get("label", "trash")
        top_score = float(top_pred.get("score", 0.0))

        primary_guidance = resolve_disposal_guidance(top_label, top_score)
        alternative_preds = map_predictions(raw_preds)

        return ClassifyResponse(
            success=True,
            inference_engine=f"Local ViT ({self.model_id}) [CPU-edge]",
            inference_time_ms=latency_ms,
            primary_result=primary_guidance,
            alternative_predictions=alternative_preds
        )

    def _to_pil_image(self, image_input: Any) -> Image.Image:
        if isinstance(image_input, Image.Image):
            return image_input.convert("RGB")
        elif isinstance(image_input, (bytes, bytearray)):
            bio = io.BytesIO(image_input)
            img = Image.open(bio)
            return img.convert("RGB")
        elif hasattr(image_input, "read"):
            bio = io.BytesIO(image_input.read())
            img = Image.open(bio)
            return img.convert("RGB")
        else:
            raise TypeError(f"Unsupported image input type: {type(image_input)}")

def get_classifier() -> WasteClassifier:
    return WasteClassifier.get_instance()
