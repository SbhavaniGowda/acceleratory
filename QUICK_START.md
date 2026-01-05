# Quick Start Guide

## Prerequisites Check

docker --version # Docker 20.10+
kubectl version --client # 1.28+
helm version # 3.10+
minikube version # latest


## Complete Setup (One Command)

chmod +x scripts/setup.sh
./scripts/setup.sh


This will:
1. ✅ Start Minikube cluster
2. ✅ Add Helm repositories
3. ✅ Create Kubernetes namespaces
4. ✅ Build AI service Docker image
5. ✅ Install Prometheus stack
6. ✅ Deploy mock microservices
7. ✅ Deploy AI observability service
8. ✅ Configure Grafana dashboards
9. ✅ Setup port forwarding

**Total time: 5-10 minutes**

## Access Services

After setup completes, access:

| Service | URL | Credentials |
|---------|-----|-------------|
| Prometheus | http://localhost:9090 | - |
| Grafana | http://localhost:3000 | admin / admin123 |
| AI Service API | http://localhost:5000 | - |

## Verify Installation

./scripts/verify.sh


## View Dashboards

1. Open Grafana: http://localhost:3000
2. Login: admin / admin123
3. Go to Dashboards → AI-Driven Anomaly Detection
4. Wait 2-3 minutes for metrics to appear

## View Logs

AI Service logs
./scripts/logs.sh ai-service

Prometheus logs
./scripts/logs.sh prometheus

All logs
./scripts/logs.sh all


## Trigger Manual Detection

curl -X POST http://localhost:5000/detect

## Cleanup

./scripts/cleanup.sh

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
