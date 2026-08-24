# BinCat | Premium Token Manager & Dashboard

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Dashboard-000000.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

## Overview
BinCat is a robust token management system designed for secure token generation, database auditing, and validation. This project leverages encryption, detailed log audit trails, and modular Python components to offer a flexible SDK for managing tokens in modern applications. It includes an interactive, glassmorphic **Web Dashboard** and a developer-friendly REST API.

---

## Features
- **Secure Token Standards**:
  - Generates tokens using **Fernet** (symmetric cryptography standard).
  - Generates stateful claims-based **JWT** (JSON Web Tokens) with cryptographic signatures.
- **Web Dashboard**:
  - Futuristic dark-themed dashboard to generate, validate, and revoke tokens.
  - Interactive metrics: Total, Active, Revoked, and Expired token counts.
  - Real-time logging console to trace SDK actions.
- **Token Lifecycle Control**:
  - Supports manual token revocation to immediately invalidate a session.
  - Custom expiration intervals (configurable via slider/API).
- **Zero Configuration Setup**:
  - Automatically generates cryptographically secure keys in `.env` if none are found.

---

## Project Structure
```
.env                    # Environment credentials (auto-generated)
.gitignore
app.py                  # Flask Application (Web Dashboard & REST APIs)
bincat_tokens.db        # SQLite database storing token registers (auto-created)
LICENSE
main.py                 # Interactive CLI token tool
README.md
requirements.txt        # Dependency definitions
setup.py                # Package specification

bincat/                 # Core SDK Package
  __init__.py
  encryption_manager.py # Cryptographic driver (Fernet & JWT)
  token_manager.py      # Database registry, validation, and logs

templates/              # Frontend templates
  index.html            # Single-Page glassmorphic dashboard UI

tools/
  encryption_key_gen.py # Key generation helper
  purge.py              # Log/DB reset script

tests/                  # Isolated Unit Tests
  __init__.py
  test_bincat.py
  test_encryption_manager.py
  test_token_manager.py
```

---

## Installation

### Prerequisites
- Python 3.10 or later
- `pip` for package management

### Steps
1. Clone the repository and navigate into it:
   ```bash
   git clone https://github.com/eduolihez/BinCat.git
   cd BinCat
   ```

2. (Optional) Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### 🚀 Running the Web Dashboard (Recommended)
Launch the Flask development server:
```bash
python app.py
```
Open your browser and navigate to **`http://localhost:5000`** to view the interactive dashboard.

### 💻 Running the CLI Application
If you prefer a terminal interface, execute:
```bash
python main.py
```

---

## REST API Endpoints
All API payloads must be sent as `application/json`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| **GET** | `/api/tokens` | Retrieve list of all tokens with metadata (status, type, creation, duration). |
| **POST** | `/api/tokens/generate` | Generate a token. Body: `{"token_type": "fernet\|jwt", "expiration_minutes": 30, "description": "text"}`. |
| **POST** | `/api/tokens/validate` | Check if a token is valid. Body: `{"token": "token_string"}`. |
| **POST** | `/api/tokens/revoke` | Revoke a token immediately. Body: `{"token": "token_string"}`. |
| **POST** | `/api/tokens/purge` | Permanently wipe database entries and delete log files. |
| **GET** | `/api/logs` | Fetch the last 50 entries of log activity. |

---

## Testing
Unit tests run in an isolated SQLite environment and do not pollute your development database. Run them using:
```bash
python -m unittest discover -s tests
```

---

## Security
`.env` holds the `ENCRYPTION_KEY` that encrypts every Fernet token in your database — it is
generated automatically on first run and is listed in `.gitignore`. Never commit your real
`.env`; use `.env.example` as a template. If a key is ever exposed, rotate it (delete `.env`
and let BinCat regenerate one) — tokens encrypted under the old key will need to be reissued.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
