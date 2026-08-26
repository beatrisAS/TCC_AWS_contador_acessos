import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from local.server import app, COUNTER_FILE  # noqa: E402


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setattr("local.server.COUNTER_FILE", tmp_path / "counter.txt")
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_counter_starts_at_zero(client):
    response = client.get("/hits")
    assert response.status_code == 200
    assert response.get_json()["total"] == 0


def test_post_increments_counter(client):
    first = client.post("/hits")
    second = client.post("/hits")
    assert first.get_json()["total"] == 1
    assert second.get_json()["total"] == 2


def test_reset_counter(client):
    client.post("/hits")
    response = client.post("/reset")
    assert response.get_json()["total"] == 0
