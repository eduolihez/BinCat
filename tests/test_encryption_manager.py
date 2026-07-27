import os
import unittest
import datetime
import jwt

from bincat.encryption_manager import EncryptionManager

class TestEncryptionManagerFernet(unittest.TestCase):
    def setUp(self):
        # Configuración para utilizar Fernet
        os.environ['ENCRYPTION_ALGORITHM'] = 'fernet'
        from cryptography.fernet import Fernet
        self.key = Fernet.generate_key().decode()
        os.environ['FERNET_KEY'] = self.key

    def tearDown(self):
        if 'ENCRYPTION_ALGORITHM' in os.environ:
            del os.environ['ENCRYPTION_ALGORITHM']
        if 'FERNET_KEY' in os.environ:
            del os.environ['FERNET_KEY']

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
        self.secret = 'mi_super_secreto'
        os.environ['JWT_SECRET'] = self.secret

    def tearDown(self):
        if 'ENCRYPTION_ALGORITHM' in os.environ:
            del os.environ['ENCRYPTION_ALGORITHM']
        if 'JWT_SECRET' in os.environ:
            del os.environ['JWT_SECRET']

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
            # Expirado hace 10 segundos usando timezone-aware UTC datetime
            'exp': datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=10)
        }
        token = jwt.encode(payload, secret, algorithm='HS256')
        if isinstance(token, bytes):
            token = token.decode()
        em = EncryptionManager()
        decrypted_text = em.decrypt(token)
        self.assertIsNone(decrypted_text, "El token expirado debe retornar None al desencriptar")

if __name__ == '__main__':
    unittest.main()
