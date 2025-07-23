from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel

from ..auth.router import get_current_user
from ..auth.service import roles_db

router = APIRouter(prefix="/api/v1/actions")

class SmsPayload(BaseModel):
    phone: str
    message: str

@router.post("/send_followup_sms")
def send_followup(payload: SmsPayload, user: str | None = Depends(get_current_user), request: Request = None):
    if not user or roles_db.get(user) != "admin":
        raise HTTPException(status_code=403, detail="forbidden")
    # Mock integration with SMS provider
    return {"sent": True, "to": payload.phone}
