import time
import os
import sys
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.auth import service
from app.audit import service as audit_service

client = TestClient(app)


def test_request_link_bad_email():
    resp = client.post("/api/v1/auth/request-link", json={"email": "not-an-email"})
    assert resp.status_code == 422


def test_token_expiry(monkeypatch):
    monkeypatch.setattr(service, "TOKEN_TTL", 1)
    token = service.create_token("a@example.com")
    time.sleep(2)
    resp = client.get(f"/api/v1/auth/callback?token={token}")
    assert resp.status_code == 400


def test_login_flow(monkeypatch):
    captured = {}

    def fake_send(email: str, token: str):
        captured["token"] = token

    monkeypatch.setattr(service, "send_magic_link", fake_send)
    import importlib
    router_module = importlib.import_module("app.auth.router")
    monkeypatch.setattr(router_module, "send_magic_link", fake_send)
    resp = client.post("/api/v1/auth/request-link", json={"email": "user@example.com"})
    assert resp.status_code == 200
    token = captured["token"]
    resp = client.get(f"/api/v1/auth/callback?token={token}")
    assert resp.status_code == 200
    assert resp.cookies.get("jwt")
    events = client.get("/api/v1/audit/events", cookies={"jwt": resp.cookies.get("jwt")})
    assert events.status_code == 403  # not admin


def test_revoke_session(monkeypatch):
    token = service.create_token("admin@example.com")
    resp = client.get(f"/api/v1/auth/callback?token={token}")
    cookie = resp.cookies.get("jwt")
    sessions = client.get("/api/v1/auth/sessions", cookies={"jwt": cookie})
    jti = next(iter(sessions.json()))
    delete = client.delete(f"/api/v1/auth/sessions/{jti}", cookies={"jwt": cookie})
    assert delete.status_code == 200
    who = client.get("/api/v1/auth/whoami", cookies={"jwt": cookie})
    assert who.status_code == 401


def test_role_gate(monkeypatch):
    service.roles_db["admin@example.com"] = "admin"
    token = service.create_token("admin@example.com")
    resp = client.get(f"/api/v1/auth/callback?token={token}")
    cookie = resp.cookies.get("jwt")
    r = client.post(
        "/api/v1/auth/roles",
        json={"name": "editor", "description": "Editor"},
        cookies={"jwt": cookie},
    )
    assert r.status_code == 200
    events = audit_service.get_events(1)
    assert events[0]["action"] == "role_create"


def test_rate_limit(monkeypatch):
    from app.middleware import ratelimit
    ratelimit._requests.clear()
    for _ in range(3):
        client.post("/api/v1/auth/request-link", json={"email": "rate@example.com"})
    r = client.post("/api/v1/auth/request-link", json={"email": "rate@example.com"})
    assert r.status_code == 429
