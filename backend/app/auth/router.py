from fastapi import APIRouter, HTTPException, Response, Depends, Request
from pydantic import BaseModel, EmailStr

from .service import (
    create_token,
    verify_token,
    send_magic_link,
    create_jwt,
    decode_jwt,
    list_sessions,
    revoke_session,
    roles_db,
    user_roles,
    create_role,
    delete_role,
    assign_role,
)
from ..middleware.ratelimit import rate_limit
from ..audit import log_event

router = APIRouter(prefix="/api/v1/auth")


def require_role(request: Request, role: str) -> None:
    """Utility to enforce role based on middleware populated data."""
    if request.state.role != role:
        raise HTTPException(status_code=403, detail="forbidden")


class EmailRequest(BaseModel):
    email: EmailStr


def _rate_key(req: Request, email: str) -> str:
    return f"{req.client.host}:{email}"


@router.post("/request-link")
@rate_limit(3, 60, lambda req, payload, **_: _rate_key(req, payload.email))
def request_link(payload: EmailRequest, request: Request):
    token = create_token(payload.email)
    try:
        send_magic_link(payload.email, token)
    except Exception as e:  # pragma: no cover - sending errors
        raise HTTPException(status_code=500, detail="email failed")
    return {"sent": True}


@router.get("/callback")
def callback(token: str, response: Response):
    email = verify_token(token)
    if not email:
        log_event(None, "login_fail", {"token": token})
        raise HTTPException(status_code=400, detail="invalid or expired token")
    jwt_token = create_jwt(email)
    log_event(email, "login_success", {})
    response.set_cookie("jwt", jwt_token, httponly=True)
    return {"logged_in": True}


def get_current_user(request: Request) -> str | None:
    cookie = request.cookies.get("jwt")
    if not cookie:
        return None
    return decode_jwt(cookie)


@router.get("/whoami")
def whoami(user: str | None = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="unauthenticated")
    return {"email": user, "role": roles_db.get(user, "user")}


@router.get("/sessions")
def list_user_sessions(request: Request, user: str | None = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="unauthenticated")
    require_role(request, roles_db.get(user, "user"))
    return list_sessions(user)


@router.delete("/sessions/{jti}")
def revoke(request: Request, jti: str, user: str | None = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="unauthenticated")
    sessions = list_sessions(user)
    if jti not in sessions:
        raise HTTPException(status_code=404, detail="not found")
    revoke_session(jti)
    return {"revoked": jti}


class RoleIn(BaseModel):
    name: str
    description: str


@router.post("/roles")
def create_role_endpoint(request: Request, payload: RoleIn, user: str | None = Depends(get_current_user)):
    if not user or roles_db.get(user) != "admin":
        raise HTTPException(status_code=403, detail="forbidden")
    create_role(payload.name, payload.description)
    log_event(user, "role_create", {"role": payload.name})
    return {"created": payload.name}


@router.get("/roles")
def list_roles(request: Request, user: str | None = Depends(get_current_user)):
    if not user or roles_db.get(user) != "admin":
        raise HTTPException(status_code=403, detail="forbidden")
    return roles_db


@router.delete("/roles/{name}")
def delete_role_endpoint(name: str, user: str | None = Depends(get_current_user)):
    if not user or roles_db.get(user) != "admin":
        raise HTTPException(status_code=403, detail="forbidden")
    delete_role(name)
    log_event(user, "role_delete", {"role": name})
    return {"deleted": name}


@router.post("/roles/{name}/assign")
def assign_role_endpoint(name: str, email: EmailStr, user: str | None = Depends(get_current_user)):
    if not user or roles_db.get(user) != "admin":
        raise HTTPException(status_code=403, detail="forbidden")
    assign_role(email, name)
    log_event(user, "role_assign", {"role": name, "user": email})
    return {"assigned": name, "user": email}

