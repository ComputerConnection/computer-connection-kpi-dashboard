from fastapi.testclient import TestClient
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.auth import service

client = TestClient(app)


def test_send_followup_sms_requires_admin():
    token = service.create_token('user@example.com')
    resp = client.get(f'/api/v1/auth/callback?token={token}')
    cookie = resp.cookies.get('jwt')
    r = client.post('/api/v1/actions/send_followup_sms', json={'phone': '123', 'message': 'hi'}, cookies={'jwt': cookie})
    assert r.status_code == 403


def test_send_followup_sms_ok():
    service.roles_db['admin@example.com'] = 'admin'
    token = service.create_token('admin@example.com')
    resp = client.get(f'/api/v1/auth/callback?token={token}')
    cookie = resp.cookies.get('jwt')
    r = client.post('/api/v1/actions/send_followup_sms', json={'phone': '123', 'message': 'hi'}, cookies={'jwt': cookie})
    assert r.status_code == 200
    assert r.json()['sent'] is True
