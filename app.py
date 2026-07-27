from flask import Flask, jsonify, request, render_template_string, render_template
import os
import sqlite3
from bincat.token_manager import TokenManager, log_event
from dotenv import load_dotenv

# Cargar/Asegurar archivo .env
load_dotenv()
if not os.getenv("ENCRYPTION_KEY"):
    from cryptography.fernet import Fernet
    generated_key = Fernet.generate_key().decode()
    with open(".env", "a") as f:
        f.write(f"\nENCRYPTION_KEY={generated_key}\n")
    # Recargar de nuevo para el proceso actual
    os.environ["ENCRYPTION_KEY"] = generated_key
    load_dotenv()

app = Flask(__name__)

# Inicializar TokenManager
token_manager = TokenManager()

@app.route("/")
def index():
    """Servir el panel de control."""
    try:
        return render_template("index.html")
    except Exception:
        # Fallback por si la plantilla no está en la carpeta de templates
        return jsonify({"error": "Templates folder or index.html missing."}), 404

@app.route("/api/tokens", methods=["GET"])
def get_tokens():
    """Obtener todos los tokens almacenados y sus estados."""
    try:
        tokens = token_manager.get_all_tokens()
        return jsonify(tokens)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/tokens/generate", methods=["POST"])
def generate_token():
    """Generar un nuevo token."""
    try:
        data = request.get_json() or {}
        token_type = data.get("token_type", "fernet").lower()
        expiration_minutes = int(data.get("expiration_minutes", 30))
        description = data.get("description", "").strip()

        if token_type not in ["fernet", "jwt"]:
            return jsonify({"status": "error", "message": "Unsupported token type. Use 'fernet' or 'jwt'."}), 400

        token = token_manager.generate_token(
            token_type=token_type,
            expiration_minutes=expiration_minutes,
            description=description
        )

        return jsonify({
            "status": "success",
            "token": token,
            "token_type": token_type,
            "expiration_minutes": expiration_minutes,
            "description": description
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/tokens/validate", methods=["POST"])
def validate_token():
    """Validar un token y devolver detalles."""
    try:
        data = request.get_json() or {}
        token = data.get("token", "").strip()
        custom_expiration = data.get("expiration_minutes")

        if not token:
            return jsonify({"status": "error", "message": "Token parameter is required."}), 400

        if custom_expiration is not None:
            custom_expiration = int(custom_expiration)

        is_valid = token_manager.is_token_valid(token, expiration_minutes=custom_expiration)

        # Buscar detalles en la DB
        details = {}
        with sqlite3.connect(token_manager.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT created_at, token_type, description, expiration_minutes, revoked FROM tokens WHERE token = ?", (token,))
            row = cursor.fetchone()
            if row:
                created_at, token_type, description, db_exp, revoked = row
                details = {
                    "created_at": created_at,
                    "token_type": token_type,
                    "description": description,
                    "db_expiration_minutes": db_exp,
                    "revoked": bool(revoked)
                }

        return jsonify({
            "status": "success",
            "is_valid": is_valid,
            "details": details
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/tokens/revoke", methods=["POST"])
def revoke_token():
    """Revocar un token."""
    try:
        data = request.get_json() or {}
        token = data.get("token", "").strip()

        if not token:
            return jsonify({"status": "error", "message": "Token parameter is required."}), 400

        success = token_manager.revoke_token(token)
        if success:
            return jsonify({"status": "success", "message": "Token revoked successfully."})
        else:
            return jsonify({"status": "error", "message": "Token not found or already revoked."}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/tokens/purge", methods=["POST"])
def purge_system():
    """Restablecer el sistema completo (logs y base de datos)."""
    try:
        success = token_manager.purge_all()
        if success:
            log_event("System Purge", "All tokens and log history cleared.")
            return jsonify({"status": "success", "message": "System purged successfully."})
        else:
            return jsonify({"status": "error", "message": "Failed to purge the system."}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/logs", methods=["GET"])
def get_logs():
    """Obtener las últimas líneas del archivo de logs."""
    log_file_path = "bincat.log"
    try:
        if not os.path.exists(log_file_path):
            return jsonify([])

        with open(log_file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        
        # Retornar las últimas 50 líneas
        last_lines = [line.strip() for line in lines[-50:]]
        return jsonify(last_lines)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    print("Starting BinCat Web Dashboard on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
