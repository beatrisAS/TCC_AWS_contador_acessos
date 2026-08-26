from pathlib import Path
from threading import Lock

from flask import Flask, jsonify, send_from_directory

app = Flask(__name__, static_folder=None)
COUNTER_FILE = Path(__file__).with_name("counter.txt")
LOCK = Lock()


def read_counter():
    if not COUNTER_FILE.exists():
        return 0
    return int(COUNTER_FILE.read_text(encoding="utf-8").strip() or "0")


def increment_counter():
    with LOCK:
        total = read_counter() + 1
        COUNTER_FILE.write_text(str(total), encoding="utf-8")
        return total


@app.post("/hits")
def register_hit():
    total = increment_counter()
    return jsonify({"message": "Acesso registrado", "total": total})


@app.get("/hits")
def get_hits():
    return jsonify({"total": read_counter()})


@app.post("/reset")
def reset_hits():
    with LOCK:
        COUNTER_FILE.write_text("0", encoding="utf-8")
    return jsonify({"message": "Contador reiniciado", "total": 0})


@app.get("/")
def home():
    frontend_dir = Path(__file__).resolve().parents[1] / "frontend"
    return send_from_directory(frontend_dir, "index.html")


@app.get("/<path:filename>")
def frontend_files(filename):
    frontend_dir = Path(__file__).resolve().parents[1] / "frontend"
    return send_from_directory(frontend_dir, filename)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
