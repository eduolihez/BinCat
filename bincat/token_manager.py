import base64
import bcrypt
import secrets
import sqlite3
import uuid
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(
    filename="bincat.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_event(event, detail):
    """Log events into the log file."""
    logging.info(f"{event}: {detail}")

class TokenManager:
    def __init__(self, db_path="bincat_tokens.db"):
        self.db_path = db_path
        self.encryption_key = Fernet.generate_key()  # Generate a new key for encryption
        self.cipher_suite = Fernet(self.encryption_key)
        self._initialize_database()

    def _initialize_database(self):
        """Create the database and the tokens table if not already created."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tokens (
                    token TEXT PRIMARY KEY,
                    hashed_token TEXT,
                    created_at TEXT,
                    revoked INTEGER DEFAULT 0
                )
            """)
            conn.commit()

    def _hash_token(self, token):
        """Hash the token with bcrypt for additional security."""
        salt = bcrypt.gensalt()
        hashed_token = bcrypt.hashpw(token.encode(), salt)
        return hashed_token

    def generate_token(self):
        """Generate a new token, encrypt it, and store it securely."""
        user_id = str(uuid.uuid4())
        random_string = secrets.token_urlsafe(8)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        token = f"{user_id}.{random_string}.{timestamp}"

        # Encrypt the token
        encrypted_token = self.cipher_suite.encrypt(token.encode()).decode()
        hashed_token = self._hash_token(token).decode()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tokens (token, hashed_token, created_at) VALUES (?, ?, ?)",
                           (encrypted_token, hashed_token, timestamp))
            conn.commit()

        log_event("Token Generated", f"Token (encrypted): {encrypted_token}")
        return encrypted_token

    def revoke_token(self, encrypted_token):
        """Revoke a token by marking it as revoked in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE tokens SET revoked = 1 WHERE token = ?", (encrypted_token,))
            conn.commit()
            revoked = cursor.rowcount > 0
            log_event("Token Revoked", f"Token (encrypted): {encrypted_token}, Revoked: {revoked}")
            return revoked

    def is_token_valid(self, encrypted_token, expiration_minutes=30):
        """Validate a token's authenticity and expiration."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT hashed_token, created_at, revoked FROM tokens WHERE token = ?", (encrypted_token,))
            row = cursor.fetchone()
            if not row:
                return False

            hashed_token, created_at, revoked = row
            if revoked:
                return False

            # Decrypt the token
            try:
                decrypted_token = self.cipher_suite.decrypt(encrypted_token.encode()).decode()
            except Exception:
                log_event("Invalid Token Decryption", f"Failed to decrypt token: {encrypted_token}")
                return False

            # Check expiration
            token_time = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            if datetime.now() - token_time > timedelta(minutes=expiration_minutes):
                return False

            # Verify the hashed token
            return bcrypt.checkpw(decrypted_token.encode(), hashed_token.encode())
