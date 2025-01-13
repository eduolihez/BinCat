import sqlite3
import base64
import secrets
import os
import logging
import uuid

from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Configuración de logging
logging.basicConfig(
    filename="bincat.log",  # Nombre del archivo de log
    level=logging.INFO,  # Nivel de log (INFO, DEBUG, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato del log
)

def log_event(event, detail):
    """Registra eventos en el archivo de logs."""
    logging.info(f"{event}: {detail}")

# Cargar variables de entorno del archivo .env
load_dotenv()

class TokenManager:
    def __init__(self, db_path="bincat_tokens.db"):
        self.db_path = db_path
        
        # Obtener la clave de cifrado del archivo .env
        encryption_key = os.getenv("ENCRYPTION_KEY")
        if not encryption_key:
            raise ValueError("ENCRYPTION_KEY is missing. Please add it to your .env file.")
        
        self.cipher = Fernet(encryption_key.encode())  # Crear un objeto Fernet con la clave
        self._initialize_database()

    def _initialize_database(self):
        """Crea la tabla de tokens si no existe."""
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
        """Genera un token cifrado y lo guarda en la base de datos."""
        user_id = str(uuid.uuid4())
        random_string = secrets.token_urlsafe(8)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        encoded_timestamp = base64.urlsafe_b64encode(timestamp.encode()).decode()

        # Crear el token sin cifrar
        raw_token = f"{base64.urlsafe_b64encode(user_id.encode()).decode()}.{random_string}.{encoded_timestamp}"
        
        # Cifrar el token
        encrypted_token = self.cipher.encrypt(raw_token.encode()).decode()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tokens (token, created_at) VALUES (?, ?)", (encrypted_token, timestamp))
            conn.commit()

        # Registrar el evento en los logs
        log_event("Token Generated", f"Token: {encrypted_token}, Timestamp: {timestamp}")
        return encrypted_token

    def revoke_token(self, token):
        """Revoca un token en la base de datos."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE tokens SET revoked = 1 WHERE token = ?", (token,))
            conn.commit()
            revoked = cursor.rowcount > 0
            log_event("Token Revoked", f"Token: {token}, Revoked: {revoked}")
            return revoked

    def is_token_valid(self, token, expiration_minutes=30):
        """Valida si un token es válido y no ha expirado."""
        try:
            # Desencriptar el token
            decrypted_token = self.cipher.decrypt(token.encode()).decode()
            parts = decrypted_token.split('.')
            if len(parts) != 3:
                return False

            encoded_timestamp = parts[2]
            timestamp = base64.urlsafe_b64decode(encoded_timestamp.encode()).decode()
            token_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            
            # Validar si el token ha expirado
            if datetime.now() - token_time > timedelta(minutes=expiration_minutes):
                return False

            # Comprobar si el token está revocado
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT revoked FROM tokens WHERE token = ?", (token,))
                row = cursor.fetchone()
                if not row or row[0] == 1:
                    return False

            return True
        except Exception as e:
            log_event("Token Validation Error", str(e))
            return False
