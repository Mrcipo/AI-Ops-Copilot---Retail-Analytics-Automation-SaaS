# AI Ops Copilot - Retail Analytics Automation SaaS

## Requisitos
- Docker + Docker Compose

## Setup
1) Copiar variables de entorno:
   - cp .env.example .env

2) Levantar el entorno:
   - docker compose up --build

## Migraciones (Alembic)
- Ejecutar migraciones dentro del contenedor backend:
  - docker compose exec backend alembic upgrade head

## Smoke test
- Backend healthcheck:
  - curl http://localhost:8000/api/v1/health
- DB ping:
  - curl http://localhost:8000/api/v1/db/ping
- Frontend (UI):
  - http://localhost:5173
