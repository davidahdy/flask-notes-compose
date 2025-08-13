import os
import logging
from flask import Flask, request, jsonify, render_template, redirect, url_for, abort
import mysql.connector
from mysql.connector import pooling, Error as MySQLError

def create_app():
    app = Flask(__name__)

    # Config via env (12-factor)
    app.config.update(
        DB_HOST=os.getenv("DB_HOST", "db"),
        DB_PORT=int(os.getenv("DB_PORT", "3306")),
        DB_USER=os.getenv("DB_USER", "notesuser"),
        DB_PASSWORD=os.getenv("DB_PASSWORD", "changeme"),
        DB_NAME=os.getenv("DB_NAME", "notesdb"),
    )

    # Basic logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    # Connection pool to MySQL
    dbcfg = dict(
        host=app.config["DB_HOST"],
        port=app.config["DB_PORT"],
        user=app.config["DB_USER"],
        password=app.config["DB_PASSWORD"],
        database=app.config["DB_NAME"],
        autocommit=True,
    )
    pool = pooling.MySQLConnectionPool(pool_name="notes_pool", pool_size=5, **dbcfg)

    def ensure_table():
        with pool.get_connection() as conn, conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB;
            """)

    # Try once at startup; healthz will verify again
    try:
        ensure_table()
        app.logger.info("DB table ensured.")
    except MySQLError as e:
        app.logger.warning(f"DB init skipped at startup: {e}")

    # Routes
    @app.get("/")
    def index():
        try:
            with pool.get_connection() as conn, conn.cursor(dictionary=True) as cur:
                cur.execute("SELECT id, content, created_at FROM notes ORDER BY created_at DESC, id DESC;")
                notes = cur.fetchall()
        except MySQLError as e:
            notes = []
            app.logger.error(f"Index DB error: {e}")
        return render_template("index.html", notes=notes)

    @app.post("/notes")
    def create_note():
        # Accept JSON or form
        content = (request.json or {}).get("content") if request.is_json else request.form.get("content")
        if not content or not content.strip():
            return jsonify({"error": "content must not be empty"}), 400
        try:
            with pool.get_connection() as conn, conn.cursor() as cur:
                cur.execute("INSERT INTO notes (content) VALUES (%s);", (content.strip(),))
                note_id = cur.lastrowid
            # If called from UI form, redirect back to home
            if not request.is_json:
                return redirect(url_for("index"), code=303)
            return jsonify({"id": note_id, "content": content.strip()}), 201
        except MySQLError as e:
            app.logger.error(f"Create DB error: {e}")
            return jsonify({"error": "database error"}), 500

    @app.get("/notes")
    def list_notes():
        try:
            with pool.get_connection() as conn, conn.cursor(dictionary=True) as cur:
                cur.execute("SELECT id, content, created_at FROM notes ORDER BY created_at DESC, id DESC;")
                rows = cur.fetchall()
            return jsonify(rows), 200
        except MySQLError as e:
            app.logger.error(f"List DB error: {e}")
            return jsonify({"error": "database error"}), 500

    @app.get("/healthz")
    def healthz():
        try:
            with pool.get_connection() as conn, conn.cursor() as cur:
                # Check connectivity and that migrations (table) are applied
                cur.execute("SELECT 1 FROM notes LIMIT 1;")
                cur.fetchall()  # ✅ Consume any remaining results to avoid "Unread result found"
            return jsonify({"status": "ok"}), 200
        except MySQLError as e:
            app.logger.warning(f"Health not ready: {e}")
            return jsonify({"status": "unhealthy", "detail": str(e)}), 503

    # Simple error handler example
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "not found"}), 404

    return app
