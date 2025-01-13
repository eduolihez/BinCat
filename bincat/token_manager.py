import base64
import secrets
import uuid
from datetime import datetime, timedelta

class TokenManager:
    def __init__(self):
        self.active_tokens = {}  # Diccionario para almacenar tokens activos
        self.logs = []

    def generate_token(self):
        """Genera un nuevo token único con un UUID, cadena aleatoria y marca de tiempo."""
        user_id = str(uuid.uuid4())
        random_string = secrets.token_urlsafe(8)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        encoded_timestamp = base64.urlsafe_b64encode(timestamp.encode()).decode()
        token = f"{base64.urlsafe_b64encode(user_id.encode()).decode()}.{random_string}.{encoded_timestamp}"
        self.active_tokens[token] = {"created_at": timestamp, "revoked": False}
        self.log_event("Token generated", token)
        return token

    def revoke_token(self, token):
        """Revoca un token específico, marcándolo como inválido."""
        if token in self.active_tokens and not self.active_tokens[token]["revoked"]:
            self.active_tokens[token]["revoked"] = True
            self.log_event("Token revoked", token)
            return True
        return False

    def is_token_valid(self, token, expiration_minutes=30):
        """Valida un token comprobando su existencia, estado y expiración."""
        try:
            if token not in self.active_tokens or self.active_tokens[token]["revoked"]:
                return False

            # Decodificar y verificar el tiempo
            _, _, encoded_timestamp = token.split('.')
            timestamp = base64.urlsafe_b64decode(encoded_timestamp.encode()).decode()
            token_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            if datetime.now() - token_time < timedelta(minutes=expiration_minutes):
                return True
        except Exception as e:
            self.log_event("Validation error", str(e))
        return False

    def list_active_tokens(self):
        """Devuelve una lista de tokens activos (no revocados)."""
        return {token: info for token, info in self.active_tokens.items() if not info["revoked"]}

    def log_event(self, event, detail):
        """Registra eventos relacionados con tokens en el historial."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {event}: {detail}"
        self.logs.append(log_entry)
        print(log_entry)  # También imprime el evento en la consola

    def save_logs_to_file(self, filepath="token_logs.txt"):
        """Guarda el historial de eventos en un archivo de texto."""
        with open(filepath, "w") as log_file:
            log_file.write("\n".join(self.logs))
