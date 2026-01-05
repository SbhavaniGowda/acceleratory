#!/bin/bash
echo ">>> Starting Minikube..."
minikube start --driver=docker
minikube addons enable metrics-server

echo ">>> Setting up Helm repositories..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
