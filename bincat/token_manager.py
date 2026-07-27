import sqlite3
import base64
import secrets
import os
import logging
import uuid
from datetime import datetime, timedelta

from bincat.encryption_manager import EncryptionManager
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

# Configuración de logging
logging.basicConfig(
    filename="bincat.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_event(event, detail):
    """Registra eventos en el archivo de logs."""
    logging.info(f"{event}: {detail}")

class TokenManager:
    def __init__(self, db_path="bincat_tokens.db"):
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        """Crea la tabla de tokens y asegura que existan todas las columnas necesarias."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tokens (
                    token TEXT PRIMARY KEY,
                    created_at TEXT,
                    revoked INTEGER DEFAULT 0
                )
            """)
            
            # Migraciones seguras para columnas adicionales
            columns_to_add = [
                ("token_type", "TEXT DEFAULT 'fernet'"),
                ("description", "TEXT DEFAULT ''"),
                ("expiration_minutes", "INTEGER DEFAULT 30")
            ]
            for col_name, col_def in columns_to_add:
                try:
                    cursor.execute(f"ALTER TABLE tokens ADD COLUMN {col_name} {col_def}")
                except sqlite3.OperationalError:
                    # La columna ya existe
                    pass
            conn.commit()

    def generate_token(self, token_type=None, expiration_minutes=30, description=""):
        """Genera un token cifrado/firmado y lo guarda en la base de datos."""
        # Si no se especifica token_type, usar el valor por defecto del entorno o 'fernet'
        if not token_type:
            token_type = os.getenv("ENCRYPTION_ALGORITHM", "fernet").lower()

        # Instanciar el EncryptionManager para este tipo específico
        enc_manager = EncryptionManager(algorithm=token_type)

        user_id = str(uuid.uuid4())
        random_string = secrets.token_urlsafe(8)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        encoded_timestamp = base64.urlsafe_b64encode(timestamp.encode()).decode()

        # Crear el token sin cifrar
        raw_token = f"{base64.urlsafe_b64encode(user_id.encode()).decode()}.{random_string}.{encoded_timestamp}"
        
        # Cifrar/firmar el token (convertimos minutos a horas para la expiración de JWT si aplica)
        expiration_hours = max(1, expiration_minutes // 60)
        encrypted_token = enc_manager.encrypt(raw_token, expiration_hours=expiration_hours)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tokens (token, created_at, token_type, description, expiration_minutes) VALUES (?, ?, ?, ?, ?)",
                (encrypted_token, timestamp, token_type, description, expiration_minutes)
            )
            conn.commit()

        log_event("Token Generated", f"Token: {encrypted_token}, Type: {token_type}, Description: '{description}', Expiration: {expiration_minutes}m")
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

    def is_token_valid(self, token, expiration_minutes=None):
        """Valida si un token es válido y no ha expirado o sido revocado."""
        try:
            # 1. Comprobar base de datos
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT revoked, created_at, expiration_minutes, token_type FROM tokens WHERE token = ?", (token,))
                row = cursor.fetchone()
                if not row:
                    return False
                revoked, created_at, db_exp_min, token_type = row
                if revoked == 1:
                    return False

            # 2. Desencriptar/Verificar firma
            enc_manager = EncryptionManager(algorithm=token_type)
            decrypted_token = enc_manager.decrypt(token)
            if not decrypted_token:
                return False

            # 3. Validar expiración de tiempo
            exp_min = expiration_minutes if expiration_minutes is not None else db_exp_min
            token_time = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            if datetime.now() - token_time > timedelta(minutes=exp_min):
                return False

            return True
        except Exception as e:
            log_event("Token Validation Error", str(e))
            return False

    def list_active_tokens(self):
        """Devuelve una lista de tokens válidos."""
        active = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT token FROM tokens WHERE revoked = 0")
            rows = cursor.fetchall()
            for row in rows:
                token = row[0]
                if self.is_token_valid(token):
                    active.append(token)
        return active

    @property
    def active_tokens(self):
        """Propiedad para compatibilidad con las pruebas unitarias existentes."""
        return self.list_active_tokens()

    def get_all_tokens(self):
        """Obtiene todos los tokens de la base de datos con sus metadatos y estado actual."""
        tokens_list = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT token, created_at, revoked, token_type, description, expiration_minutes FROM tokens ORDER BY created_at DESC")
            rows = cursor.fetchall()
            for row in rows:
                token, created_at, revoked, token_type, description, expiration_minutes = row
                
                # Calcular estado
                is_valid = self.is_token_valid(token)
                
                # Chequear si ha expirado para clasificarlo
                token_time = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                expired = datetime.now() - token_time > timedelta(minutes=expiration_minutes)
                
                status = "active"
                if revoked == 1:
                    status = "revoked"
                elif expired:
                    status = "expired"
                elif not is_valid:
                    status = "invalid"

                tokens_list.append({
                    "token": token,
                    "created_at": created_at,
                    "revoked": bool(revoked),
                    "token_type": token_type,
                    "description": description,
                    "expiration_minutes": expiration_minutes,
                    "status": status
                })
        return tokens_list

    def save_logs_to_file(self, filename):
        """Guarda una copia de los logs en el archivo destino especificado."""
        log_file_path = "bincat.log"
        try:
            if os.path.exists(log_file_path):
                import shutil
                shutil.copy(log_file_path, filename)
                return True
            else:
                with open(filename, "w") as f:
                    f.write("")
                return True
        except Exception as e:
            log_event("Save Logs Error", str(e))
            return False

    def purge_all(self):
        """Limpia la base de datos y borra el archivo de logs."""
        try:
            # Vaciar base de datos
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM tokens")
                conn.commit()
            
            # Borrar logs
            log_file_path = "bincat.log"
            if os.path.exists(log_file_path):
                os.remove(log_file_path)
            return True
        except Exception as e:
            print(f"Purge error: {e}")
            return False
