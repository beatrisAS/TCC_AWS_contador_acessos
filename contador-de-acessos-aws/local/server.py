"""API local para demonstrar o contador sem AWS, Docker ou LocalStack.

Fluxo equivalente para a apresentação:
Navegador -> API local -> função de incremento -> arquivo JSON persistente.
"""
from __future__ import annotations

import json
from pathlib import Path
from threading import Lock

from flask import Flask, jsonify

APP_DIR = Path(__file__).resolve().parent
DATA_FILE = APP_DIR / "data.json"
LOCK = Lock()

app = Flask(__name__)


@app.after_request
def permitir_frontend(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


def ler_total() -> int:
    if not DATA_FILE.exists():
        return 0
    try:
        dados = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        return int(dados.get("acessos", 0))
    except (json.JSONDecodeError, ValueError, TypeError):
        return 0


def salvar_total(total: int) -> None:
    DATA_FILE.write_text(
        json.dumps({"id": "hits", "acessos": total}, indent=2),
        encoding="utf-8",
    )


def resposta(total: int):
    return jsonify({"id": "hits", "total_acessos": total, "acessos": total, "modo": "simulacao-offline"})


@app.get("/api/acessos")
def consultar_acessos():
    with LOCK:
        return resposta(ler_total())


@app.post("/api/acessos")
def registrar_acesso():
    with LOCK:
        total = ler_total() + 1
        salvar_total(total)
        return resposta(total), 200


@app.post("/api/reset")
def resetar_acessos():
    with LOCK:
        salvar_total(0)
        return resposta(0)


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "servico": "contador-local"})


@app.errorhandler(404)
def nao_encontrado(_erro):
    return jsonify({"erro": "rota não encontrada"}), 404


if __name__ == "__main__":
    print("API local: http://127.0.0.1:5000")
    print("Health:    http://127.0.0.1:5000/api/health")
    app.run(host="127.0.0.1", port=5000, debug=True)
