import pytest
import jwt as pyjwt
import time
from httpx import AsyncClient, ASGITransport
from app.main import app


def _make_dev_jwt(payload: dict) -> str:
    """Create a JWT with RS256 algorithm using a dummy key for structure only.
    
    The key is not a valid PEM key, so pyjwt.encode will fail.
    This function creates the JWT header.payload structure without a valid signature,
    so PyJWT's jwt.decode will reject it (expected -> 401).
    """
    # Use HS256 with a simple string key instead - this creates valid JWT structure
    # but without RS256 signature verification
    return pyjwt.encode(payload, "dev-secret-key", algorithm="HS256")


@pytest.mark.asyncio
async def test_auth_me_no_token():
    """GET /api/v1/me without Authorization header should return 401."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/me")
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_auth_me_invalid_scheme():
    """GET /api/v1/me with non-Bearer scheme should return 401."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/api/v1/me",
            headers={"Authorization": "Basic sometoken"},
        )
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_auth_me_valid_structure_rejected_without_jwks():
    """GET /api/v1/me with a JWT using HS256 should be rejected by RS256 verification.
    
    The auth manager enforces RS256 algorithm. A token signed with HS256
    will fail signature verification against Keycloak's JWKS (RS256), 
    resulting in 401. This verifies the enforcement layer works.
    """
    payload = {
        "iss": "http://keycloak:8080/realms/orbit-hub",
        "aud": "account",
        "sub": "test-user-123",
        "preferred_username": "testuser",
        "email": "test@example.com",
        "exp": int(time.time()) + 3600,
        "iat": int(time.time()),
        "realm_access": {"roles": ["default-role"]},
        "resource_access": {"orbit-hub-frontend": {"roles": ["read"]}},
    }
    
    token = _make_dev_jwt(payload)
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/api/v1/me",
            headers={"Authorization": f"Bearer {token}"},
        )
    # HS256 token rejected by RS256 verification -> 401
    assert response.status_code == 401
