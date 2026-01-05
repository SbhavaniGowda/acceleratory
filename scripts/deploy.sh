#!/bin/bash
# Point shell to Minikube's docker-daemon
eval $(minikube -p minikube docker-env)

echo ">>> Building Images..."
docker build -t ai-service:latest ./docker/ai-service
docker build -t mock-service:latest ./docker/mock-service

echo ">>> Applying Manifests..."
kubectl apply -f kubernetes/namespaces.yaml
kubectl apply -f kubernetes/ai-service/
kubectl apply -f kubernetes/mock-services.yaml

echo ">>> Installing Monitoring Stack (Helm)..."
helm install prometheus prometheus-community/prometheus \
  --namespace accelerator-ops -f helm/prometheus-values.yaml

helm install grafana grafana/grafana \
  --namespace accelerator-ops -f helm/grafana-values.yaml
