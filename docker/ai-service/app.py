from flask import Flask, request, jsonify, Response
import time
import random

from prometheus_client import (
    generate_latest,
    Counter,
    Gauge,
    Histogram,
    CONTENT_TYPE_LATEST
)

app = Flask(__name__)

# =========================================================
# METRICS DEFINITIONS
# =========================================================

# 1️⃣ Total prediction requests (Traffic)
REQUEST_COUNTER = Counter(
    "ai_prediction_requests_total",
    "Total number of prediction requests"
)

# 2️⃣ AI predictions made (Business metric)
PREDICTION_COUNTER = Counter(
    "ai_predictions_total",
    "Total number of AI predictions made",
    ["model"]
)

# 3️⃣ Inference latency (Latency + P99 + Heatmap)
INFERENCE_LATENCY = Histogram(
    "ai_inference_processing_seconds",
    "Time spent processing inference",
    buckets=(0.1, 0.2, 0.5, 1, 2, 5)
)

# 4️⃣ Model confidence (Gauge)
MODEL_CONFIDENCE = Gauge(
    "ai_model_confidence",
    "Current confidence level of the model"
)

# 5️⃣ Anomaly detection with root cause
ANOMALY_COUNTER = Counter(
    "ai_anomalies_detected_total",
    "Detected AI anomalies",
    ["root_cause"]
)

# 6️⃣ GPU utilization (mocked for demo)
GPU_UTILIZATION = Gauge(
    "ai_accelerator_gpu_utilization",
    "GPU utilization percentage"
)

# 7️⃣ GPU temperature (mocked for demo)
GPU_TEMPERATURE = Gauge(
    "ai_accelerator_temperature_celsius",
    "GPU temperature in Celsius"
)

# =========================================================
# ROUTES
# =========================================================

@app.route("/metrics")
def metrics():
    """Expose Prometheus metrics."""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/predict", methods=["POST"])
def predict():
    """
    Simulated AI prediction endpoint with observability.
    """

    # Count request
    REQUEST_COUNTER.inc()

    start_time = time.time()

    # Simulate inference latency
    with INFERENCE_LATENCY.time():
        processing_time = random.uniform(0.1, 0.6)
        time.sleep(processing_time)

    # Mock prediction
    prediction = "normal"
    confidence = random.uniform(0.85, 0.99)

    # Simulate GPU stats
    gpu_util = random.uniform(30, 95)
    gpu_temp = random.uniform(55, 90)

    GPU_UTILIZATION.set(gpu_util)
    GPU_TEMPERATURE.set(gpu_temp)

    # Detect anomalies
    if confidence < 0.7:
        prediction = "anomaly"
        ANOMALY_COUNTER.labels(root_cause="low_confidence").inc()

    if processing_time > 0.5:
        ANOMALY_COUNTER.labels(root_cause="latency_spike").inc()

    if gpu_util > 85:
        ANOMALY_COUNTER.labels(root_cause="gpu_saturation").inc()

    if gpu_temp > 80:
        ANOMALY_COUNTER.labels(root_cause="gpu_overheat").inc()

    # Update metrics
    PREDICTION_COUNTER.labels(model="anomaly_detector").inc()
    MODEL_CONFIDENCE.set(confidence)

    return jsonify({
        "status": "success",
        "prediction": prediction,
        "confidence": round(confidence, 3),
        "latency_seconds": round(processing_time, 3),
        "gpu_utilization": round(gpu_util, 2),
        "gpu_temperature": round(gpu_temp, 2)
    })


# =========================================================
# APP START
# =========================================================

if __name__ == "__main__":
    print("🚀 Starting AI Service on port 5001")
    print("📊 Metrics available at http://localhost:5001/metrics")
    app.run(host="0.0.0.0", port=5001)
