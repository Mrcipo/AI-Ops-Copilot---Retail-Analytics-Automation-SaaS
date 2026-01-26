# AI Ops Copilot - Retail Analytics Automation SaaS

## Requisitos
- Docker + Docker Compose

## Setup
1) Copiar variables de entorno:
   - cp .env.example .env

2) Levantar el entorno:
   - docker compose up --build

## Smoke test
- Backend healthcheck:
  - curl http://localhost:8000/api/v1/health
- Frontend (UI):
  - http://localhost:5173
