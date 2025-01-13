from bincat.token_manager import TokenManager

manager = TokenManager()

# Generar un token
token = manager.generate_token()
print("Generated Token:", token)

# Verificar si el token es válido
print("Is Token Valid?", manager.is_token_valid(token))

# Revocar el token
manager.revoke_token(token)
print("Is Token Valid after revocation?", manager.is_token_valid(token))

# Listar tokens activos
active_tokens = manager.list_active_tokens()
print("Active Tokens:", active_tokens)

# Guardar logs en un archivo
manager.save_logs_to_file("token_logs.txt")
