import base64
import secrets
import uuid
from datetime import datetime, timedelta
import sqlite3

class TokenManager:
    def __init__(self, db_path="bincat_tokens.db"):
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        """Crea la tabla para almacenar los tokens si no existe."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tokens (
                    token TEXT PRIMARY KEY,
                    created_at TEXT,
                    revoked INTEGER DEFAULT 0
                )
            """)
            conn.commit()

    def generate_token(self):
        """Genera un nuevo token y lo almacena en la base de datos."""
        user_id = str(uuid.uuid4())
        random_string = secrets.token_urlsafe(8)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        encoded_timestamp = base64.urlsafe_b64encode(timestamp.encode()).decode()
        token = f"{base64.urlsafe_b64encode(user_id.encode()).decode()}.{random_string}.{encoded_timestamp}"

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tokens (token, created_at) VALUES (?, ?)", (token, timestamp))
            conn.commit()

        return token

    def revoke_token(self, token):
        """Revoca un token marcándolo como inválido en la base de datos."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE tokens SET revoked = 1 WHERE token = ?", (token,))
            conn.commit()
            return cursor.rowcount > 0  # Devuelve True si el token fue revocado

    def is_token_valid(self, token, expiration_minutes=30):
        """Valida un token comprobando su existencia, estado y expiración."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT created_at, revoked FROM tokens WHERE token = ?", (token,))
            row = cursor.fetchone()
            if not row:
                return False  # El token no existe

            created_at, revoked = row
            if revoked:
                return False  # El token está revocado

            token_time = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            return datetime.now() - token_time < timedelta(minutes=expiration_minutes)

    def list_active_tokens(self):
        """Lista todos los tokens activos (no revocados)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT token, created_at FROM tokens WHERE revoked = 0")
            return cursor.fetchall()

    def cleanup_expired_tokens(self, expiration_minutes=30):
        """Elimina los tokens expirados de la base de datos."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            expiration_threshold = datetime.now() - timedelta(minutes=expiration_minutes)
            cursor.execute("DELETE FROM tokens WHERE created_at <= ?", (expiration_threshold.strftime("%Y-%m-%d %H:%M:%S"),))
            conn.commit()
