from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(f"Your encryption key is: {key.decode()}")

# Guarda esta clave en un archivo .env o en un lugar seguro
