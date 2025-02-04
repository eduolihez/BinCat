# encryption_manager.py

import os
import datetime
from cryptography.fernet import Fernet
import jwt

class EncryptionManager:
    def __init__(self):
        # Lee la variable para seleccionar el algoritmo (por defecto 'fernet')
        self.algorithm = os.getenv('ENCRYPTION_ALGORITHM', 'fernet').lower()

        if self.algorithm == 'fernet':
            self.key = os.getenv('FERNET_KEY')
            if not self.key:
                raise Exception("La variable FERNET_KEY no está configurada.")
            self.cipher = Fernet(self.key)
        elif self.algorithm == 'jwt':
            self.jwt_secret = os.getenv('JWT_SECRET')
            if not self.jwt_secret:
                raise Exception("La variable JWT_SECRET no está configurada.")
        else:
            raise Exception(f"Algoritmo de encriptación '{self.algorithm}' no soportado.")

    def encrypt(self, data: str) -> str:
        """
        Encripta el dato (en formato string) usando el algoritmo configurado.
        """
        if self.algorithm == 'fernet':
            # Retorna el token codificado como string
            return self.cipher.encrypt(data.encode()).decode()
        elif self.algorithm == 'jwt':
            # Genera un payload con una expiración (por ejemplo, 1 hora)
            payload = {
                'data': data,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }
            token = jwt.encode(payload, self.jwt_secret, algorithm='HS256')
            # jwt.encode puede retornar un string o bytes según la versión de PyJWT
            if isinstance(token, bytes):
                token = token.decode()
            return token

    def decrypt(self, token: str) -> str:
        """
        Desencripta el token según el algoritmo configurado.
        Devuelve el dato original o None en caso de error.
        """
        if self.algorithm == 'fernet':
            try:
                return self.cipher.decrypt(token.encode()).decode()
            except Exception as e:
                # Manejo de errores según convenga
                return None
        elif self.algorithm == 'jwt':
            try:
                decoded = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
                return decoded.get('data')
            except jwt.ExpiredSignatureError:
                # Token expirado
                return None
            except jwt.InvalidTokenError:
                # Token inválido
                return None
