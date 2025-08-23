from flask import Blueprint, request, jsonify
import sqlite3

group_bp = Blueprint("group", __name__, url_prefix="/group")

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Obtener grupos
@group_bp.route("/", methods=["GET"])
def get_groups():
    conn = get_db_connection()
    groups = conn.execute("SELECT * FROM groups").fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in groups])

# Crear un grupo
@group_bp.route("/", methods=["POST"])
def create_group():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")

    if not name:
        return jsonify({"error": "Falta el nombre"}), 400

    conn = get_db_connection()
    conn.execute("INSERT INTO groups (name, description) VALUES (?, ?)", (name, description))
    conn.commit()
    conn.close()

    return jsonify({"message": "Grupo creado correctamente"}), 201
