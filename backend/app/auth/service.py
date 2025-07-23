import os
import smtplib
import uuid
import time
from email.message import EmailMessage

import jwt

# Mail configuration for sending login links
MAIL_HOST = os.getenv("MAIL_HOST", "mailhog")
MAIL_PORT = int(os.getenv("MAIL_PORT", "1025"))
MAIL_FROM = os.getenv("MAIL_FROM", "noreply@example.com")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "secret")
TOKEN_TTL = int(os.getenv("TOKEN_TTL", "900"))

# In-memory stores used in tests/local dev
_tokens: dict[str, dict] = {}
_sessions: dict[str, dict] = {}

# role name -> description mapping
roles_db: dict[str, str] = {}
# user email -> role name mapping
user_roles: dict[str, str] = {}


def send_magic_link(email: str, token: str) -> None:
    """Send the login link to the provided email."""
    msg = EmailMessage()
    msg["Subject"] = "Your login link"
    msg["From"] = MAIL_FROM
    msg["To"] = email
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    link = f"{base_url}/api/v1/auth/callback?token={token}"
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
    """Create a JWT and track it as an active session."""
    jti = uuid.uuid4().hex
    payload = {"sub": email, "jti": jti}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    _sessions[jti] = {"email": email, "exp": time.time() + TOKEN_TTL}
    return token


def decode_jwt(token: str) -> str | None:
    """Decode a JWT and ensure the session is still active."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None
    jti = payload.get("jti")
    if not jti or jti not in _sessions:
        return None
    if _sessions[jti]["exp"] < time.time():
        _sessions.pop(jti, None)
        return None
    return payload.get("sub")


def list_sessions(email: str | None = None) -> dict[str, dict]:
    """Return active sessions, optionally filtered by user email."""
    if email:
        return {j: s for j, s in _sessions.items() if s["email"] == email}
    return dict(_sessions)


def revoke_session(jti: str) -> None:
    """Invalidate a session token."""
    _sessions.pop(jti, None)


def create_role(name: str, description: str) -> None:
    roles_db[name] = description


def delete_role(name: str) -> None:
    roles_db.pop(name, None)
    for user, role in list(user_roles.items()):
        if role == name:
            user_roles[user] = "user"


def assign_role(email: str, role: str) -> None:
    if role not in roles_db:
        raise ValueError("role not found")
    user_roles[email] = role
