# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

auth-oidc

## Roadmap

### continue-implementation — Continue implementation and resolve known failures

Status: done

Acceptance:
- Run checks, fix failures, and implement the next planned feature

Implementation: `frontend/src/components/ModelCard.tsx`, `frontend/src/components/ModelRegistry.tsx`, `frontend/src/index.css`

Tests: `backend/tests/test_models.py`, `frontend/src/components/HealthStatus.test.tsx`

### auth-oidc — OIDC authentication with Keycloak

Status: in_progress

Acceptance:
- Keycloak integration in docker-compose
- Backend validates JWT tokens
- Frontend login/logout flow
- Protected API endpoints

Implementation: `backend/app/api/auth_router.py - login endpoint`, `backend/app/main.py - Keycloak config in app state`, `backend/app/auth/manager.py - JWT validation with RS256`

Tests: `backend/tests/test_auth.py - existing auth tests`

