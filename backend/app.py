from flask import Flask
from routes.church import church_bp
from routes.group import group_bp
from routes.post import post_bp
from routes.user import user_bp
from models.church import init_db as init_church_db
from models.user import init_user_db
from models.group import init_group_db
from models.post import init_post_db

app = Flask(__name__)

# Registrar blueprints
app.register_blueprint(church_bp)
app.register_blueprint(group_bp)
app.register_blueprint(post_bp)
app.register_blueprint(user_bp)

@app.route("/")
def home():
    return "Bienvenido a AmenLink API 🙌"

if __name__ == "__main__":
    # Inicializar todas las tablas
    init_church_db()
    init_user_db()
    init_group_db()
    init_post_db()
    app.run(debug=True)