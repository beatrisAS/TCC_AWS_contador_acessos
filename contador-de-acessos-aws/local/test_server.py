import json

import server


def test_contador_incrementa_e_reseta(tmp_path, monkeypatch):
    arquivo = tmp_path / "data.json"
    monkeypatch.setattr(server, "DATA_FILE", arquivo)
    cliente = server.app.test_client()

    assert cliente.get("/api/health").status_code == 200
    assert cliente.get("/api/acessos").get_json()["total_acessos"] == 0
    assert cliente.post("/api/acessos").get_json()["total_acessos"] == 1
    assert cliente.post("/api/acessos").get_json()["total_acessos"] == 2
    assert json.loads(arquivo.read_text(encoding="utf-8"))["acessos"] == 2
    assert cliente.post("/api/reset").get_json()["total_acessos"] == 0
