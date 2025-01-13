import uuid
import secrets
import base64
from datetime import datetime

def generate_token():
    user_id = str(uuid.uuid4())  # Genera un ID único en formato UUID
    random_string = secrets.token_urlsafe(8)  # Cadena aleatoria segura
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Marca de tiempo actual
    encoded_timestamp = base64.urlsafe_b64encode(timestamp.encode()).decode()
    token = f"{base64.urlsafe_b64encode(user_id.encode()).decode()}.{random_string}.{encoded_timestamp}"
    return token
