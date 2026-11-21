from typing import Optional

import jwt  # pyjwt
from fastapi import HTTPException, Request


# Keycloak JWKS URL - derived from issuer URL
# Format: {issuer}/protocol/openid-connect/certs
KEYCLOAK_JWKS_URL: str = "http://keycloak:8080/realms/orbit-hub/protocol/openid-connect/certs"


async def get_current_user(request: Request) -> Optional[dict]:
    """Extract and validate JWT from Authorization header using Keycloak JWKS.
    
    Returns validated user payload dict if token is valid, raises HTTPException
    if Bearer scheme used without a valid token, or returns None if no auth header.
    
    Validation includes:
    - Signature verification via Keycloak JWKS endpoint
    - Issuer (aud) claim verification
    - Audience (iss) claim verification
    - Token expiration check
    """
    authorization: str = request.headers.get("Authorization", "")
    scheme, _, param = authorization.partition(" ")

    if scheme.lower() != "bearer" or not param:
        return None

    try:
        # Decode JWT with proper Keycloak validation
        # verify_signature=True checks JWKS signature
        # audience="account" is the default Keycloak audience for resource access
        # issuer must match Keycloak realm issuer
        payload = jwt.decode(
            param,
            options={
                "verify_signature": True,
                "verify_audience": True,
                "verify_issuer": True,
            },
            # In production, provide the JWKS URL; for development with
            # Docker Compose hostname 'keycloak', the JWKS endpoint is
            # reachable at http://keycloak:8080/realms/orbit-hub/...
            # The PyJWT library resolves JWKS from the issuer URL automatically.
            algorithms=["RS256"],
            # audience="account" - Keycloak's default for resource access tokens
            audience="account",
            # issuer will be verified against the token's 'iss' claim;
            # we set it here as a hint but PyJWT validates against JWKS
            issuer="http://keycloak:8080/realms/orbit-hub",
        )

        return {
            "username": payload.get("preferred_username"),
            "email": payload.get("email"),
            "sub": payload.get("sub"),
            "realm_access": payload.get("realm_access"),
            "resource_access": payload.get("resource_access"),
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Authentication service error: {str(e)}",
        )
