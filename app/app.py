import os
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def db_config():
    return {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "appuser"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "appdb"),
    }

def get_connection():
    return mysql.connector.connect(**db_config())

def ensure_schema():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS notes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        message VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit(); cur.close(); conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        message = request.form.get("message", "").strip()
        if message:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("INSERT INTO notes (message) VALUES (%s)", (message,))
            conn.commit(); cur.close(); conn.close()
        return redirect(url_for("home"))
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT id, message, created_at FROM notes ORDER BY id DESC")
    notes = cur.fetchall(); cur.close(); conn.close()
    return render_template("index.html", notes=notes)

@app.get("/health")
def health():
    try:
        conn = get_connection(); conn.close()
        return {"status": "ok", "database": "reachable"}, 200
    except Exception as exc:
        return {"status": "error", "database": str(exc)}, 500

if __name__ == "__main__":
    ensure_schema(); app.run(host="0.0.0.0", port=5000)
