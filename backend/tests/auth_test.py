import time
import os
import sys
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.auth import service

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
