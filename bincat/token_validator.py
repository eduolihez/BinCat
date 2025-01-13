import base64
from datetime import datetime, timedelta

def is_token_valid(token, expiration_minutes=30):
    try:
        # Divide el token en partes
        encoded_id, random_string, encoded_timestamp = token.split('.')
        # Decodifica y analiza el timestamp
        timestamp = base64.urlsafe_b64decode(encoded_timestamp.encode()).decode()
        token_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        # Verifica si el token aún está dentro del tiempo válido
        if datetime.now() - token_time < timedelta(minutes=expiration_minutes):
            return True
    except Exception as e:
        print(f"Error validando el token: {e}")
    return False
