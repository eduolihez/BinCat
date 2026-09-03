# BinCat

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Dashboard-000000.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

### [Versión en Español](README.md) · **[English version](README.en.md)**

BinCat generates, validates and revokes authentication tokens, and keeps an
audit trail of every operation. It ships as a Python SDK you can drop into an
application, plus a web dashboard and a REST API on top of it.

## Features

It issues two kinds of token: Fernet, using symmetric cryptography, and
cryptographically signed JWTs carrying stateful claims. Expiration intervals
are configurable from the dashboard slider or the API, and any token can be
revoked by hand to kill a session immediately.

The dashboard is a dark-themed single page where you generate, validate and
revoke tokens. It shows counts of total, active, revoked and expired tokens,
and a logging console that traces SDK actions as they happen.

There is nothing to configure before the first run. If BinCat finds no keys in
`.env`, it generates cryptographically secure ones.

## Project structure

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

## Installation

You need Python 3.10 or later and `pip`.

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

## Usage

Start the Flask development server and open `http://localhost:5000` for the
dashboard:

```bash
python app.py
```

There is also a terminal interface, if you would rather stay in the shell:

```bash
python main.py
```

## REST API endpoints

Send all payloads as `application/json`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tokens` | Retrieve list of all tokens with metadata (status, type, creation, duration). |
| POST | `/api/tokens/generate` | Generate a token. Body: `{"token_type": "fernet\|jwt", "expiration_minutes": 30, "description": "text"}`. |
| POST | `/api/tokens/validate` | Check if a token is valid. Body: `{"token": "token_string"}`. |
| POST | `/api/tokens/revoke` | Revoke a token immediately. Body: `{"token": "token_string"}`. |
| POST | `/api/tokens/purge` | Permanently wipe database entries and delete log files. |
| GET | `/api/logs` | Fetch the last 50 entries of log activity. |

## Testing

The tests run against an isolated SQLite database, so they leave your
development one alone:

```bash
python -m unittest discover -s tests
```

## Security

`.env` holds the `ENCRYPTION_KEY` that encrypts every Fernet token in your
database. BinCat generates it on first run and `.gitignore` already covers it.
Never commit your real `.env`; use `.env.example` as a template. If a key ever
leaks, delete `.env` and let BinCat regenerate one, then reissue the tokens that
were encrypted under the old key.

## License

MIT. See the `LICENSE` file for details.
