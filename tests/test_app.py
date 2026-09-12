import json

from local_api import server


def test_contador_incrementa_e_persiste(tmp_path, monkeypatch):
    arquivo = tmp_path / "data.json"
    monkeypatch.setattr(server, "DATA_FILE", arquivo)
    client = server.app.test_client()

    assert client.get("/api/health").status_code == 200
    assert client.get("/api/acessos").get_json()["total_acessos"] == 0
    assert client.post("/api/acessos").get_json()["total_acessos"] == 1
    assert client.post("/api/acessos").get_json()["total_acessos"] == 2
    assert json.loads(arquivo.read_text()) == {"id": "hits", "acessos": 2}
    assert client.post("/api/reset").get_json()["total_acessos"] == 0
