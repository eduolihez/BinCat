import os
import datetime
from cryptography.fernet import Fernet
import jwt

class EncryptionManager:
    def __init__(self, algorithm=None, key=None, jwt_secret=None):
        # Fallback to env variables if not provided
        self.algorithm = (algorithm or os.getenv('ENCRYPTION_ALGORITHM', 'fernet')).lower()

        if self.algorithm == 'fernet':
            # Support both FERNET_KEY and ENCRYPTION_KEY (default key name in .env)
            self.key = key or os.getenv('FERNET_KEY') or os.getenv('ENCRYPTION_KEY')
            if not self.key:
                raise ValueError("Fernet key is missing (provide key, FERNET_KEY or ENCRYPTION_KEY).")
            
            if isinstance(self.key, str):
                self.key_bytes = self.key.encode()
            else:
                self.key_bytes = self.key
                self.key = self.key.decode()
                
            self.cipher = Fernet(self.key_bytes)
        elif self.algorithm == 'jwt':
            # Support JWT_SECRET or fallback to ENCRYPTION_KEY
            self.jwt_secret = jwt_secret or os.getenv('JWT_SECRET') or os.getenv('ENCRYPTION_KEY')
            if not self.jwt_secret:
                raise ValueError("JWT secret is missing (provide jwt_secret, JWT_SECRET or ENCRYPTION_KEY).")
        else:
            raise ValueError(f"Unsupported encryption algorithm: {self.algorithm}")

    def encrypt(self, data: str, expiration_hours: int = 1) -> str:
        """Encrypts data (string format) using the configured algorithm."""
        if self.algorithm == 'fernet':
            return self.cipher.encrypt(data.encode()).decode()
        elif self.algorithm == 'jwt':
            # Generate a payload with expiration using timezone-aware UTC datetime
            payload = {
                'data': data,
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=expiration_hours)
            }
            token = jwt.encode(payload, self.jwt_secret, algorithm='HS256')
            if isinstance(token, bytes):
                token = token.decode()
            return token

    def decrypt(self, token: str) -> str:
        """Decrypts a token. Returns the original string or None on failure or expiration."""
        if self.algorithm == 'fernet':
            try:
                return self.cipher.decrypt(token.encode()).decode()
            except Exception:
                return None
        elif self.algorithm == 'jwt':
            try:
                decoded = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
                return decoded.get('data')
            except jwt.ExpiredSignatureError:
                return None
            except jwt.InvalidTokenError:
                return None
