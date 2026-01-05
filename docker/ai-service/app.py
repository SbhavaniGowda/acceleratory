from flask import Flask, request, jsonify, Response
import time
import random
from prometheus_client import generate_latest, Counter, Gauge, CONTENT_TYPE_LATEST
 
app = Flask(__name__)
 
# --- METRICS DEFINITION ---
# 1. Counter for total predictions
PREDICTION_COUNTER = Counter(
    'ai_predictions_total', 
    'Total number of AI predictions made',
    ['model']
)
 
# 2. Gauge for model confidence
CONFIDENCE_GAUGE = Gauge(
    'ai_model_confidence', 
    'Current confidence level of the model'
)
 
@app.route('/metrics')
def metrics():
    """
    Expose Prometheus metrics on /metrics endpoint.
    """
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
 
@app.route('/predict', methods=['POST'])
def predict():
    """
    Simulates an AI prediction endpoint.
    """
    # Increment the counter for every request
    PREDICTION_COUNTER.labels(model='anomaly_detector').inc()
    
    # Simulate processing delay
    time.sleep(random.uniform(0.1, 0.5))
    
    # Mock logic
    prediction = "normal"
    confidence = random.uniform(0.85, 0.99)
    
    # Randomly simulate an anomaly
    if random.random() < 0.1:
        prediction = "anomaly"
        confidence = random.uniform(0.50, 0.70)
    
    # Update the gauge with the latest confidence
    CONFIDENCE_GAUGE.set(confidence)
        
    return jsonify({
        "status": "success",
        "prediction": prediction,
        "confidence": confidence
    })
 
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})
 
if __name__ == '__main__':
    # CHANGED PORT TO 5001 to avoid conflicts
    print("Starting AI Service on port 5001...")
    print("Metrics available at: http://localhost:5001/metrics")
    app.run(host='0.0.0.0', port=5001)
 