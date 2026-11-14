from fastapi import APIRouter, Depends, HTTPException

from app.auth.manager import get_current_user

router = APIRouter(tags=["auth"])


@router.get("/me", response_model=dict)
async def read_user_me(
    current_user: dict = Depends(get_current_user),
) -> dict:
    """Get current user info from validated JWT.
    
    Returns user claims from JWT. Real Keycloak integration would verify
    signature via JWKS endpoint at {issuer}/protocol/openid-connect/certs.
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "username": current_user.get("preferred_username"),
        "email": current_user.get("email"),
        "sub": current_user.get("sub"),
    }
