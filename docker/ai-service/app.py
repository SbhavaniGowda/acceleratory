
"""
AI Observability - Flask app with Prometheus metrics

Endpoints:
  POST /predict  -> Simulated AI prediction (observability metrics recorded)
  GET  /metrics  -> Prometheus metrics in text format
  GET  /health   -> Liveness
  GET  /ready    -> Readiness
  GET  /         -> Simple greeting

Run (Windows-friendly WSGI server):
  pip install flask prometheus-client waitress
  waitress-serve --host=0.0.0.0 --port=5001 app:app

Optionally (run with Uvicorn via ASGI wrapper):
  pip install asgiref uvicorn
  uvicorn app:asgi_app --host 0.0.0.0 --port 5001
"""

import os
import time
import random
from typing import Optional

from flask import Flask, request, jsonify, Response, g
from prometheus_client import (
    generate_latest,
    Counter,
    Gauge,
    Histogram,
    CONTENT_TYPE_LATEST,
    PROCESS_COLLECTOR,
    PLATFORM_COLLECTOR,
)

# -----------------------------------------------------------------------------
# App setup
# -----------------------------------------------------------------------------
SERVICE_NAME = os.getenv("SERVICE_NAME", "ai-service")
APP_START_TIME = time.time()

app = Flask(__name__)

# -----------------------------------------------------------------------------
# Metrics (default global registry)
# -----------------------------------------------------------------------------
# Note: PROCESS_COLLECTOR and PLATFORM_COLLECTOR auto-register on import.

# 1️ Total prediction requests (Traffic)
REQUEST_COUNTER = Counter(
    "ai_prediction_requests_total",
    "Total number of prediction requests",
    labelnames=("service",),
)

# 2️ AI predictions made (Business metric)
PREDICTION_COUNTER = Counter(
    "ai_predictions_total",
    "Total number of AI predictions made",
    labelnames=("service", "model"),
)

# 3️ Inference latency (Latency + buckets)
INFERENCE_LATENCY = Histogram(
    "ai_inference_processing_seconds",
    "Time spent processing inference (seconds)",
    labelnames=("service", "model"),
    buckets=(0.1, 0.2, 0.5, 1, 2, 5),
)

# 4️ Model confidence (Gauge)
MODEL_CONFIDENCE = Gauge(
    "ai_model_confidence",
    "Current confidence level of the model",
    labelnames=("service", "model"),
)

# 5️ Anomaly detection with root cause
ANOMALY_COUNTER = Counter(
    "ai_anomalies_detected_total",
    "Detected AI anomalies",
    labelnames=("service", "root_cause"),
)

# 6️ GPU utilization (mocked for demo)
GPU_UTILIZATION = Gauge(
    "ai_accelerator_gpu_utilization",
    "GPU utilization percentage",
    labelnames=("service",),
)

# 7️ GPU temperature (mocked for demo)
GPU_TEMPERATURE = Gauge(
    "ai_accelerator_temperature_celsius",
    "GPU temperature in Celsius",
    labelnames=("service",),
)

# Generic HTTP metrics for all routes
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    labelnames=("service", "method", "path", "status"),
)

HTTP_REQUEST_LATENCY_SECONDS = Histogram(
    "http_request_latency_seconds",
    "HTTP request latency in seconds",
    labelnames=("service", "method", "path"),
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10),
)

APP_START_TIME_GAUGE = Gauge(
    "app_start_time_seconds",
    "Unix timestamp when the app started",
    labelnames=("service",),
)
APP_START_TIME_GAUGE.labels(service=SERVICE_NAME).set(APP_START_TIME)


# -----------------------------------------------------------------------------
# Request instrumentation hooks
# -----------------------------------------------------------------------------
@app.before_request
def _start_timer():
    g._start_time = time.time()


@app.after_request
def _record_metrics(response):
    try:
        method = request.method
        # Prefer Flask's route rule for stable cardinality
        rule = getattr(request, "url_rule", None)
        path: str = rule.rule if rule and hasattr(rule, "rule") else request.path
        status = response.status_code
        elapsed = time.time() - getattr(g, "_start_time", time.time())

        HTTP_REQUESTS_TOTAL.labels(
            service=SERVICE_NAME, method=method, path=path, status=status
        ).inc()

        HTTP_REQUEST_LATENCY_SECONDS.labels(
            service=SERVICE_NAME, method=method, path=path
        ).observe(elapsed)
    except Exception:
        # Do not break response flow due to metrics
        pass

    return response


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return jsonify(
        status="ok",
        service=SERVICE_NAME,
        message="Hello from ai-service",
        time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    )


@app.get("/health")
def health():
    return jsonify({"status": "healthy", "service": SERVICE_NAME})


@app.get("/ready")
def ready():
    # Customize readiness (e.g., check DB, model loaded, etc.)
    ready_after = float(os.getenv("READY_AFTER_SECONDS", "0"))
    is_ready = (time.time() - APP_START_TIME) >= ready_after
    return (
        jsonify({"status": "ready" if is_ready else "starting", "service": SERVICE_NAME}),
        200 if is_ready else 503,
    )


@app.get("/metrics")
def metrics():
    """Expose Prometheus metrics."""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.post("/predict")
def predict():
    """
    Simulated AI prediction endpoint with observability.

    Accepts JSON body (optional), e.g.:
    {
      "model": "anomaly_detector"
    }
    """
    model_name = (request.json or {}).get("model", "anomaly_detector")

    # Count request
    REQUEST_COUNTER.labels(service=SERVICE_NAME).inc()

    start_time = time.time()

    # Simulate inference latency (and observe with labels)
    processing_time = random.uniform(0.1, 0.6)
    time.sleep(processing_time)
    INFERENCE_LATENCY.labels(service=SERVICE_NAME, model=model_name).observe(processing_time)

    # Mock prediction & confidence
    prediction = "normal"
    confidence = random.uniform(0.85, 0.99)

    # Simulate GPU stats
    gpu_util = random.uniform(30, 95)
    gpu_temp = random.uniform(55, 90)
    GPU_UTILIZATION.labels(service=SERVICE_NAME).set(gpu_util)
    GPU_TEMPERATURE.labels(service=SERVICE_NAME).set(gpu_temp)

    # Anomaly rules
    if confidence < 0.7:
        prediction = "anomaly"
        ANOMALY_COUNTER.labels(service=SERVICE_NAME, root_cause="low_confidence").inc()

    if processing_time > 0.5:
        ANOMALY_COUNTER.labels(service=SERVICE_NAME, root_cause="latency_spike").inc()

    if gpu_util > 85:
        ANOMALY_COUNTER.labels(service=SERVICE_NAME, root_cause="gpu_saturation").inc()

    if gpu_temp > 80:
        ANOMALY_COUNTER.labels(service=SERVICE_NAME, root_cause="gpu_overheat").inc()

    # Update metrics
    PREDICTION_COUNTER.labels(service=SERVICE_NAME, model=model_name).inc()
    MODEL_CONFIDENCE.labels(service=SERVICE_NAME, model=model_name).set(confidence)

    return jsonify({
        "status": "success",
        "service": SERVICE_NAME,
        "model": model_name,
        "prediction": prediction,
        "confidence": round(confidence, 3),
        "latency_seconds": round(processing_time, 3),
        "gpu_utilization": round(gpu_util, 2),
        "gpu_temperature": round(gpu_temp, 2),
        "ts": time.time(),
    })


try:
    from asgiref.wsgi import WsgiToAsgi
    asgi_app = WsgiToAsgi(app)
except Exception:
    asgi_app = None


# -----------------------------------------------------------------------------
# Local dev entrypoint (python app.py)
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print(" Starting AI Service on port 5001")
    print(" Metrics available at http://localhost:5001/metrics")
    app.run(host="0.0.0.0", port=5001)
