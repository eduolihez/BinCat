import logging
import sqlite3
import uuid
import secrets
import base64
from datetime import datetime, timedelta

# Configuración de logging
logging.basicConfig(
    filename="bincat.log",  # Nombre del archivo de log
    level=logging.INFO,  # Nivel de log (INFO, DEBUG, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato del log
)

def log_event(event, detail):
    """Registra eventos en el archivo de logs."""
    logging.info(f"{event}: {detail}")

class TokenManager:
    def __init__(self, db_path="bincat_tokens.db"):
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        """Inicializa la base de datos y la tabla de tokens si no existe."""
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
        """Genera un nuevo token, lo guarda en la base de datos y lo registra en los logs."""
        user_id = str(uuid.uuid4())  # Genera un ID de usuario único
        random_string = secrets.token_urlsafe(8)  # Genera una cadena aleatoria
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Hora actual
        encoded_timestamp = base64.urlsafe_b64encode(timestamp.encode()).decode()  # Timestamp codificado
        token = f"{base64.urlsafe_b64encode(user_id.encode()).decode()}.{random_string}.{encoded_timestamp}"

        # Almacena el token en la base de datos
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tokens (token, created_at) VALUES (?, ?)", (token, timestamp))
            conn.commit()

        # Registrar el evento de generación de token
        log_event("Token Generated", f"Token: {token}, Timestamp: {timestamp}")
        return token

    def revoke_token(self, token):
        """Revoca un token existente y lo registra en los logs."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE tokens SET revoked = 1 WHERE token = ?", (token,))
            conn.commit()
            revoked = cursor.rowcount > 0  # Verifica si se revocó un token
            # Registrar el evento de revocación del token
            log_event("Token Revoked", f"Token: {token}, Revoked: {revoked}")
            return revoked

    def is_token_valid(self, token, expiration_minutes=30):
        """Verifica si un token es válido, es decir, si no ha sido revocado y no ha expirado."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT created_at, revoked FROM tokens WHERE token = ?", (token,))
            row = cursor.fetchone()
            if not row:
                return False
            created_at, revoked = row
            if revoked:
                return False
            token_time = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            # Verifica si el token no ha expirado
            return datetime.now() - token_time < timedelta(minutes=expiration_minutes)

