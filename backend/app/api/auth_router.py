from fastapi import APIRouter, Depends, HTTPException, Request, Query

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


@router.get("/login", response_model=None)
async def login(
    request: Request,
    redirect_uri: str = Query(
        ...,
        description="Callback URI registered with Keycloak",
    ),
) -> None:
    """Redirect user to Keycloak OAuth authorization page.
    
    Generates the Keycloak authorization URL with the given redirect_uri.
    The user will be redirected to Keycloak for authentication, then
    back to this redirect_uri with an authorization code.
    """
    keycloak_issuer = request.app.state.keycloak_issuer_url
    keycloak_client_id = request.app.state.keycloak_client_id
    
    # Build Keycloak authorization URL
    import urllib.parse
    import uuid
    
    state = str(uuid.uuid4())
    request.session["oauth2_state"] = state
    
    auth_url = f"{keycloak_issuer}/protocol/openid-connect/auth?" + urllib.parse.urlencode({
        "response_type": "code",
        "client_id": keycloak_client_id,
        "redirect_uri": redirect_uri,
        "scope": "openid profile email",
        "state": state,
    })
    
    raise HTTPException(status_code=307, headers={"Location": auth_url})
