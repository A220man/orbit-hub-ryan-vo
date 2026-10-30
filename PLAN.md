# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

fastapi-react-skeleton

## Roadmap

### fastapi-react-skeleton — FastAPI + React skeleton with health check

Status: done

Acceptance:
- FastAPI backend starts and serves /health endpoint
- React frontend builds and serves
- Docker compose runs both services
- Frontend displays backend health status

Implementation: `backend/app/main.py`, `backend/app/core/config.py`, `backend/app/api/health.py`, `backend/Dockerfile`, `backend/requirements.txt`, `backend/pyproject.toml`, `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/src/components/HealthStatus.tsx`, `frontend/src/api/client.ts`, `frontend/src/types/api.ts`, `frontend/vite.config.ts`, `frontend/package.json`, `frontend/Dockerfile`, `frontend/nginx.conf`, `docker-compose.yaml`, `.env.example`, `README.md`, `LICENSE`, `CHANGELOG.md`, `portfolio.json`

### core-api-workflow — Core API workflow: ML model registry with CRUD

Status: done

Acceptance:
- Create/list/get/update/delete ML models via API
- SQLite persistence with pagination and filtering
- Frontend dashboard for model registry
- Backend tests for CRUD operations

Implementation: `backend/app/models/__init__.py`, `backend/app/models/model.py`, `backend/app/schemas/__init__.py`, `backend/app/schemas/model.py`, `backend/app/api/deps.py`, `backend/app/api/models.py`, `backend/app/core/database.py`, `backend/app/main.py`, `backend/tests/test_models.py`, `backend/tests/conftest.py`

Tests: `backend/tests/test_models.py`

### auth-oidc — OIDC authentication with Keycloak

Status: planned

Acceptance:
- Keycloak integration in docker-compose
- Backend validates JWT tokens
- Frontend login/logout flow
- Protected API endpoints

### llm-adapters — LLM provider adapters (OpenAI, Anthropic, Gemini, Ollama)

Status: planned

Acceptance:
- Configurable provider selection
- Unified chat completion interface
- Mock adapter for testing
- Provider configuration documented

### ai-evaluation-workflow — AI/ML model evaluation workflow

Status: planned

Acceptance:
- Run evaluation jobs against registered models
- Store evaluation results with metrics
- Frontend displays evaluation history
- Reproducible evaluation command

