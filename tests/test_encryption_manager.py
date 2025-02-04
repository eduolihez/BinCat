import os
import sys
# Añadimos el directorio raíz del proyecto al sys.path para que se pueda importar encryption_manager
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest
import datetime
import jwt  # Requerido para la prueba de expiración en JWT

from encryption_manager import EncryptionManager

class TestEncryptionManagerFernet(unittest.TestCase):
    def setUp(self):
        # Configuración para utilizar Fernet
        os.environ['ENCRYPTION_ALGORITHM'] = 'fernet'
        # Generar una clave Fernet si no existe (se genera una nueva para cada test)
        from cryptography.fernet import Fernet
        os.environ['FERNET_KEY'] = Fernet.generate_key().decode()

    def test_encrypt_decrypt(self):
        em = EncryptionManager()
        original_text = "texto de prueba"
        token = em.encrypt(original_text)
        self.assertIsInstance(token, str, "El token debe ser un string")
        decrypted_text = em.decrypt(token)
        self.assertEqual(original_text, decrypted_text, "El texto desencriptado debe coincidir con el original")

class TestEncryptionManagerJWT(unittest.TestCase):
    def setUp(self):
        # Configuración para utilizar JWT
        os.environ['ENCRYPTION_ALGORITHM'] = 'jwt'
        os.environ['JWT_SECRET'] = 'mi_super_secreto'

    def test_encrypt_decrypt(self):
        em = EncryptionManager()
        original_text = "texto de prueba"
        token = em.encrypt(original_text)
        self.assertIsInstance(token, str, "El token JWT debe ser un string")
        decrypted_text = em.decrypt(token)
        self.assertEqual(original_text, decrypted_text, "El texto desencriptado debe coincidir con el original")

    def test_jwt_expired(self):
        # Creamos manualmente un token JWT expirado para simular la expiración
        secret = os.environ['JWT_SECRET']
        payload = {
            'data': 'texto de prueba',
            'exp': datetime.datetime.utcnow() - datetime.timedelta(seconds=1)  # Expirado hace 1 segundo
        }
        token = jwt.encode(payload, secret, algorithm='HS256')
        if isinstance(token, bytes):
            token = token.decode()
        em = EncryptionManager()
        decrypted_text = em.decrypt(token)
        self.assertIsNone(decrypted_text, "El token expirado debe retornar None al desencriptar")

if __name__ == '__main__':
    unittest.main()
