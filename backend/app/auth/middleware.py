from fastapi import Request

from .service import decode_jwt, roles_db


async def auth_middleware(request: Request, call_next):
    token = request.cookies.get("jwt")
    user = decode_jwt(token) if token else None
    request.state.user = user
    request.state.role = roles_db.get(user, "user") if user else None
    response = await call_next(request)
    return response
