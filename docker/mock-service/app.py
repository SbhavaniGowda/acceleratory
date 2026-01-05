from flask import Flask
import requests
import time
import random
import threading

app = Flask(__name__)

def background_traffic_generator():
    """Continuously sends requests to the AI service."""
    print("Starting background traffic generator...")
    while True:
        try:
            # Randomly simulate high load (anomaly) or normal load
            is_anomaly = random.choice([True, False, False, False]) # 25% chance
            
            if is_anomaly:
                payload = {"gpu_util": random.uniform(85, 100), "temp": random.uniform(85, 100)}
            else:
                payload = {"gpu_util": random.uniform(30, 60), "temp": random.uniform(50, 70)}

            # Send to AI Service (hostname 'ai-service' works in Docker Compose & K8s)
            requests.post("http://ai-service:5000/predict", json=payload, timeout=1)
        except Exception as e:
            print(f"Connection failed: {e}")
        
        time.sleep(2)

@app.route('/')
def health():
    return "Mock Service Running", 200

if __name__ == '__main__':
    # Start traffic generation in background
    thread = threading.Thread(target=background_traffic_generator)
    thread.daemon = True
    thread.start()
    
    app.run(host='0.0.0.0', port=8080)
