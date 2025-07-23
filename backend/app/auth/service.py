import os
import smtplib
import uuid
import time
from email.message import EmailMessage

import jwt

MAIL_HOST = os.getenv("MAIL_HOST", "mailhog")
MAIL_PORT = int(os.getenv("MAIL_PORT", "1025"))
MAIL_FROM = os.getenv("MAIL_FROM", "noreply@example.com")
SECRET_KEY = os.getenv("SECRET_KEY", "secret")
TOKEN_TTL = int(os.getenv("TOKEN_TTL", "900"))

_tokens: dict[str, dict] = {}
roles_db: dict[str, str] = {}


def send_magic_link(email: str, token: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = "Your login link"
    msg["From"] = MAIL_FROM
    msg["To"] = email
    link = f"http://localhost:8000/api/v1/auth/callback?token={token}"
    msg.set_content(f"Login: {link}")
    with smtplib.SMTP(MAIL_HOST, MAIL_PORT) as s:
        s.send_message(msg)


def create_token(email: str, ttl: int | None = None) -> str:
    token = uuid.uuid4().hex
    exp = time.time() + (ttl or TOKEN_TTL)
    _tokens[token] = {"email": email, "exp": exp}
    return token


def verify_token(token: str) -> str | None:
    data = _tokens.get(token)
    if not data:
        return None
    if data["exp"] < time.time():
        _tokens.pop(token, None)
        return None
    return data["email"]


def create_jwt(email: str) -> str:
    payload = {"sub": email}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_jwt(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("sub")
    except jwt.PyJWTError:
        return None
