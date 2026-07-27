import os
import sys

# Añadimos el directorio raíz del proyecto al sys.path para poder importar bincat
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from bincat.token_manager import TokenManager

def purge_logs_and_db():
    """Borra todos los logs y limpia la base de datos."""
    try:
        db_path = os.path.join(root_dir, "bincat_tokens.db")
        manager = TokenManager(db_path=db_path)
        if manager.purge_all():
            print("Logs successfully deleted.")
            print("Database successfully cleared.")
        else:
            print("Failed to clear some files.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    purge_logs_and_db()
