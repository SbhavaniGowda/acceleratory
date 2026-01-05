#!/bin/bash

# Port forward the service to localhost temporarily
echo ">>> Port forwarding ai-service..."
kubectl port-forward svc/ai-service 5000:5000 -n accelerator-ops &
PF_PID=$!

# Give it a second to establish
sleep 2

echo ">>> Sending Normal Request..."
curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"gpu_util": 50, "temp": 60}'
echo -e "\n"

echo ">>> Sending Anomaly Request (High Temp)..."
curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"gpu_util": 95, "temp": 98}'
echo -e "\n"

# Kill the port forward
kill $PF_PID
echo ">>> Test Complete."
