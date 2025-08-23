from flask import Blueprint, request, jsonify
import sqlite3

user_bp = Blueprint("users", __name__, url_prefix="/users")

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Obtener todos los usuarios
@user_bp.route("/", methods=["GET"])
def get_users():
    conn = get_db_connection()
    users = conn.execute("SELECT id, username, email FROM users").fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in users])

# Crear un usuario
@user_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Faltan datos"}), 400

    try:
        conn = get_db_connection()
        conn.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                     (username, email, password))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Usuario o email ya existe"}), 409

    return jsonify({"message": "Usuario creado con éxito"}), 201
