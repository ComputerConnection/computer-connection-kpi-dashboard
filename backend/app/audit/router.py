from fastapi import APIRouter, Depends, HTTPException, Request

from .service import get_events
from ..auth.service import roles_db

def _current_user(request: Request):
    from ..auth.router import get_current_user
    return get_current_user(request)

router = APIRouter(prefix="/api/v1/audit")


@router.get("/events")
def events(limit: int = 100, user: str | None = Depends(_current_user)):
    if not user or roles_db.get(user) != "admin":
        raise HTTPException(status_code=403, detail="forbidden")
    return get_events(limit)
