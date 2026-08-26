from __future__ import annotations

import json
from pathlib import Path
from threading import Lock

from flask import Flask, jsonify

DATA_FILE = Path(__file__).resolve().parent / "data.json"
LOCK = Lock()
app = Flask(__name__)


@app.after_request
def cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


def read_total() -> int:
    if not DATA_FILE.exists():
        return 0
    try:
        return int(json.loads(DATA_FILE.read_text(encoding="utf-8")).get("acessos", 0))
    except (json.JSONDecodeError, TypeError, ValueError):
        return 0


def write_total(total: int) -> None:
    DATA_FILE.write_text(json.dumps({"id": "hits", "acessos": total}, indent=2), encoding="utf-8")


def payload(total: int):
    return jsonify({"id": "hits", "total_acessos": total})


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/acessos")
def get_accesses():
    with LOCK:
        return payload(read_total())


@app.post("/api/acessos")
def add_access():
    with LOCK:
        total = read_total() + 1
        write_total(total)
        return payload(total)


@app.post("/api/reset")
def reset():
    with LOCK:
        write_total(0)
        return payload(0)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
