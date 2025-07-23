from fastapi.testclient import TestClient
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

client = TestClient(app)


def test_sales_daily_query():
    query = '{ salesDaily { date amount } }'
    resp = client.post('/api/v1/graphql', json={'query': query})
    assert resp.status_code == 200
    data = resp.json()['data']['salesDaily']
    assert isinstance(data, list)
    assert 'date' in data[0]


def test_quotes_funnel_query():
    query = '{ quotesFunnel { new sent won } }'
    resp = client.post('/api/v1/graphql', json={'query': query})
    assert resp.status_code == 200
    assert resp.json()['data']['quotesFunnel']['new'] == 10
