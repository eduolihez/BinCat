import unittest
import os
from bincat.token_manager import TokenManager

class TestTokenManager(unittest.TestCase):
    def setUp(self):
        # Usar una base de datos de pruebas temporal para no contaminar la principal
        self.db_path = "test_bincat_tokens.db"
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass
        self.manager = TokenManager(db_path=self.db_path)

    def tearDown(self):
        # Eliminar base de datos y archivos de logs de prueba creados
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass
        if os.path.exists("test_logs.txt"):
            try:
                os.remove("test_logs.txt")
            except OSError:
                pass

    def test_generate_token(self):
        token = self.manager.generate_token(token_type="fernet")
        self.assertIn(token, self.manager.active_tokens)

    def test_revoke_token(self):
        token = self.manager.generate_token(token_type="fernet")
        self.assertTrue(self.manager.revoke_token(token))
        self.assertFalse(self.manager.is_token_valid(token))

    def test_list_active_tokens(self):
        token1 = self.manager.generate_token(token_type="fernet")
        token2 = self.manager.generate_token(token_type="fernet")
        self.manager.revoke_token(token1)
        active_tokens = self.manager.list_active_tokens()
        self.assertIn(token2, active_tokens)
        self.assertNotIn(token1, active_tokens)

    def test_save_logs_to_file(self):
        self.manager.generate_token(token_type="fernet")
        self.manager.save_logs_to_file("test_logs.txt")
        self.assertTrue(os.path.exists("test_logs.txt"))
        with open("test_logs.txt", "r") as log_file:
            logs = log_file.readlines()
        self.assertTrue(len(logs) > 0)

    def test_jwt_token_type(self):
        token = self.manager.generate_token(token_type="jwt", expiration_minutes=60, description="Test JWT")
        self.assertIn(token, self.manager.active_tokens)
        all_tokens = self.manager.get_all_tokens()
        self.assertEqual(len(all_tokens), 1)
        self.assertEqual(all_tokens[0]["token_type"], "jwt")
        self.assertEqual(all_tokens[0]["description"], "Test JWT")
        self.assertEqual(all_tokens[0]["expiration_minutes"], 60)

if __name__ == '__main__':
    unittest.main()
