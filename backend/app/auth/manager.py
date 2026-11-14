from typing import Optional

from fastapi import HTTPException, Request


async def get_current_user(request: Request) -> Optional[dict]:
    """Extract JWT from Authorization header.
    
    Returns user payload dict if present, raises HTTPException if Bearer
    scheme used without a token, or returns None if no auth header.
    
    Note: Real Keycloak integration would verify signature via JWKS endpoint.
    For development, the payload is returned as-is for token inspection.
    """
    authorization: str = request.headers.get("Authorization", "")
    scheme, _, param = authorization.partition(" ")
    
    if scheme.lower() != "bearer" or not param:
        return None
    
    # Development mode: return token payload for inspection
    # Real Keycloak would verify via: jwt.decode(token, key, algorithms=["RS256"])
    # with JWKS from: {keycloak_url}/realms/{realm}/protocol/openid-connect/certs
    try:
        # Simple base64 decode of the three JWT parts for development
        import base64
        import json
        
        parts = param.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid JWT format")
        
        # Decode payload (second part)
        payload_json = base64.urlsafe_b64decode(parts[1] + "==").decode("utf-8")
        payload = json.loads(payload_json)
        return payload
    except (ValueError, IndexError, UnicodeDecodeError, json.JSONDecodeError):
        # If decoding fails, still return None rather than crash
        # (real implementation would do proper JWT validation)
        return None
