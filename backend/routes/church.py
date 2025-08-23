from flask import Blueprint, request, jsonify
import sqlite3

# Definimos el blueprint
church_bp = Blueprint('church', __name__, url_prefix="/church")

# Función para conectar con la DB (usa SQLite local)
def get_db_connection():
    conn = sqlite3.connect("database.db")  # podés cambiar el path si querés
    conn.row_factory = sqlite3.Row
    return conn

# Obtener todas las iglesias
@church_bp.route("/", methods=["GET"])
def get_churches():
    conn = get_db_connection()
    churches = conn.execute("SELECT * FROM churches").fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in churches])

# Crear una nueva iglesia
@church_bp.route("/", methods=["POST"])
def create_church():
    data = request.get_json()
    name = data.get("name")
    location = data.get("location")

    if not name or not location:
        return jsonify({"error": "Faltan datos"}), 400

    conn = get_db_connection()
    conn.execute("INSERT INTO churches (name, location) VALUES (?, ?)", (name, location))
    conn.commit()
    conn.close()

    return jsonify({"message": "Iglesia creada correctamente"}), 201

# Obtener una iglesia por ID
@church_bp.route("/<int:id>", methods=["GET"])
def get_church(id):
    conn = get_db_connection()
    church = conn.execute("SELECT * FROM churches WHERE id = ?", (id,)).fetchone()
    conn.close()
    if church is None:
        return jsonify({"error": "Iglesia no encontrada"}), 404
    return jsonify(dict(church))
