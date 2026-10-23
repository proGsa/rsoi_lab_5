
import os

import jwt
from jwt import PyJWKClient
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import PyJWTError

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "library-auth.uk.auth0.com").strip().rstrip("/")

AUTH0_ISSUER = os.getenv("AUTH0_ISSUER", f"https://{AUTH0_DOMAIN}/").strip()

AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "https://library-api").strip()

JWKS_URL = os.getenv("JWKS_URL", f"https://{AUTH0_DOMAIN}/.well-known/jwks.json",).strip()

jwks_client = PyJWKClient(JWKS_URL, cache_keys=True)
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)) -> dict:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="Missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=AUTH0_ISSUER,
            audience=AUTH0_AUDIENCE,
            options={
                "require": ["exp", "iss", "sub", "aud"],
            },
        )

        return payload

    except (PyJWTError, Exception) as exc:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


def get_current_username(payload: dict = Depends(get_current_user)) -> str:
    return payload["sub"]
