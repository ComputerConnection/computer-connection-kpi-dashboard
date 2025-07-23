from fastapi import APIRouter, HTTPException, Response, Depends, Request
from pydantic import BaseModel, EmailStr

from .service import (
    create_token,
    verify_token,
    send_magic_link,
    create_jwt,
    decode_jwt,
    roles_db,
)

router = APIRouter(prefix="/api/v1/auth")


class EmailRequest(BaseModel):
    email: EmailStr


@router.post("/request-link")
def request_link(payload: EmailRequest):
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
        raise HTTPException(status_code=400, detail="invalid or expired token")
    jwt_token = create_jwt(email)
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
