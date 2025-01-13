import os
import sqlite3


def purge_logs_and_db():
    """Deletes all log files and clears the database."""
    try:
        # Path to the log file in the root directory
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_path = os.path.join(root_dir, "bincat.log")
        
        if os.path.exists(log_path):
            os.remove(log_path)
            print("Logs successfully deleted.")
        else:
            print("No log file found to delete.")

        # Path to the database file in the root directory
        db_path = os.path.join(root_dir, "bincat_tokens.db")
        
        if os.path.exists(db_path):
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM tokens")
                conn.commit()
            print("Database successfully cleared.")
        else:
            print("No database file found to clear.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    purge_logs_and_db()
