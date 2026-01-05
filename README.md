# AI-Driven Observability Stack with Minikube

Production-ready monitoring stack featuring:
- **Minikube** - Local Kubernetes cluster
- **Prometheus** - Time-series metrics database
- **Grafana** - Interactive dashboards
- **AI Service** - Anomaly detection & Root Cause Analysis

## Quick Start

Clone repository
git clone <repo>
cd ai-observability-minikube

Make scripts executable
chmod +x scripts/*.sh

Run complete setup (5-10 minutes)
./scripts/setup.sh

Access services
Prometheus: http://localhost:9090
Grafana: http://localhost:3000 (admin/admin123) 
AI Service: http://localhost:5000



## System Requirements

- Docker Desktop or Docker Engine
- 6+ CPU cores
- 12+ GB RAM
- 100GB disk space
- kubectl, helm, minikube installed

## Features

✅ Automated Minikube setup
✅ Prometheus + Grafana stack
✅ AI anomaly detection (Isolation Forest)
✅ Root cause analysis (Correlation-based)
✅ Mock microservices with metrics
✅ Grafana dashboards
✅ Alert rules and notifications
✅ Complete documentation

## Architecture

┌─────────────────────────────────────┐
│ Minikube Kubernetes Cluster │
├─────────────────────────────────────┤
│ │
│ Monitoring Namespace │
│ ├─ Prometheus (9090) │
│ ├─ Grafana (3000) │
│ ├─ AlertManager (9093) │
│ └─ Node Exporter │
│ │
│ Demo Apps Namespace │
│ ├─ Payment Service (8001) │
│ ├─ Auth Service (8002) │
│ └─ API Gateway (8003) │
│ │
│ AI Observability Namespace │
│ └─ AI Service (5000, 8888) │
│ │
└─────────────────────────────────────┘


## Next Steps

1. [Quick Start](QUICK_START.md)
2. [Manual Setup](docs/MANUAL_SETUP.md)
3. [Troubleshooting](TROUBLESHOOTING.md)
4. [Advanced Configuration](docs/ADVANCED.md)
