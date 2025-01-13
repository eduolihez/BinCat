import os
import sqlite3

# Eliminar el archivo de logs
log_file = "bincat.log"
if os.path.exists(log_file):
    os.remove(log_file)
    print("Log file deleted successfully.")
else:
    print("No log file found.")

# Vaciar la base de datos
db_file = "bincat_tokens.db"
if os.path.exists(db_file):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tokens")  # Eliminar todos los registros de la tabla 'tokens'
        conn.commit()
        print("Database cleared successfully.")
else:
    print("No database file found.")
