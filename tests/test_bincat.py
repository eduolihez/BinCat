import unittest
from bincat.token_generator import generate_token
from bincat.token_validator import is_token_valid

class TestBinCat(unittest.TestCase):
    def test_generate_token(self):
        token = generate_token()
        self.assertIsInstance(token, str)
        self.assertGreater(len(token.split('.')), 2)

    def test_token_validation(self):
        token = generate_token()
        self.assertTrue(is_token_valid(token))

    def test_expired_token(self):
        token = generate_token()
        # Simular un token vencido (cambiar la validación en el módulo si lo deseas)
        self.assertFalse(is_token_valid(token, expiration_minutes=-1))

if __name__ == '__main__':
    unittest.main()
