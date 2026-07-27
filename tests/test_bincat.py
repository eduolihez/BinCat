import unittest
import os
from bincat.token_manager import TokenManager

class TestBinCat(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_bincat_main_test.db"
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass
        self.manager = TokenManager(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass

    def test_generate_token(self):
        token = self.manager.generate_token()
        self.assertIsInstance(token, str)

    def test_token_validation(self):
        token = self.manager.generate_token()
        self.assertTrue(self.manager.is_token_valid(token))

    def test_expired_token(self):
        token = self.manager.generate_token(expiration_minutes=30)
        # Validar pasando una expiración de -1 minutos para simular expiración inmediata
        self.assertFalse(self.manager.is_token_valid(token, expiration_minutes=-1))

if __name__ == '__main__':
    unittest.main()
