import unittest
from bincat.token_manager import TokenManager

class TestTokenManager(unittest.TestCase):
    def setUp(self):
        self.manager = TokenManager()

    def test_generate_token(self):
        token = self.manager.generate_token()
        self.assertIn(token, self.manager.active_tokens)

    def test_revoke_token(self):
        token = self.manager.generate_token()
        self.assertTrue(self.manager.revoke_token(token))
        self.assertFalse(self.manager.is_token_valid(token))

    def test_list_active_tokens(self):
        token1 = self.manager.generate_token()
        token2 = self.manager.generate_token()
        self.manager.revoke_token(token1)
        active_tokens = self.manager.list_active_tokens()
        self.assertIn(token2, active_tokens)
        self.assertNotIn(token1, active_tokens)

    def test_save_logs_to_file(self):
        self.manager.generate_token()
        self.manager.save_logs_to_file("test_logs.txt")
        with open("test_logs.txt", "r") as log_file:
            logs = log_file.readlines()
        self.assertTrue(len(logs) > 0)

if __name__ == '__main__':
    unittest.main()
