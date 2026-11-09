# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

continue-implementation

## Roadmap

### continue-implementation — Continue implementation and resolve known failures

Status: done

Acceptance:
- Run checks, fix failures, and implement the next planned feature

Implementation: `frontend/src/components/ModelCard.tsx`, `frontend/src/components/ModelRegistry.tsx`, `frontend/src/index.css`

Tests: `backend/tests/test_models.py`, `frontend/src/components/HealthStatus.test.tsx`

### auth-oidc — OIDC authentication with Keycloak

Status: planned

Acceptance:
- Keycloak integration in docker-compose
- Backend validates JWT tokens
- Frontend login/logout flow
- Protected API endpoints

