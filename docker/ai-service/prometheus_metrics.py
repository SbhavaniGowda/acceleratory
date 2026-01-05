from prometheus_client import Counter, Gauge, Histogram

# Metrics definitions
PREDICTION_REQUESTS = Counter(
    'ai_prediction_requests_total', 
    'Total number of prediction requests'
)
ANOMALY_DETECTED = Counter(
    'ai_anomalies_detected_total', 
    'Total number of anomalies detected',
    ['root_cause']
)
GPU_UTILIZATION = Gauge(
    'ai_accelerator_gpu_utilization', 
    'Current GPU Utilization %'
)
GPU_TEMPERATURE = Gauge(
    'ai_accelerator_temperature_celsius', 
    'Current GPU Temperature'
)
INFERENCE_TIME = Histogram(
    'ai_inference_processing_seconds', 
    'Time spent processing inference'
)
