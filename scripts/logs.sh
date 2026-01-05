#!/bin/bash
SERVICE=${1:-ai-service} # Default to ai-service if no arg provided

echo ">>> Tailing logs for $SERVICE in namespace accelerator-ops..."
POD_NAME=$(kubectl get pods -n accelerator-ops -l app=$SERVICE -o jsonpath="{.items[0].metadata.name}")

if [ -z "$POD_NAME" ]; then
    echo "Error: No pod found for app=$SERVICE"
    exit 1
fi

kubectl logs -f $POD_NAME -n accelerator-ops
