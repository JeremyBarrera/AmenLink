from flask import Blueprint, request, jsonify
import sqlite3

post_bp = Blueprint("post", __name__, url_prefix="/post")

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Obtener todos los posts
@post_bp.route("/", methods=["GET"])
def get_posts():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts").fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in posts])

# Crear un post
@post_bp.route("/", methods=["POST"])
def create_post():
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")
    user_id = data.get("user_id")

    if not title or not content or not user_id:
        return jsonify({"error": "Faltan datos"}), 400

    conn = get_db_connection()
    conn.execute("INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)", (title, content, user_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Post creado con éxito"}), 201
