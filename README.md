# BinCat

## Overview
BinCat is a robust token management system designed for secure token generation, validation, and database handling. This project leverages encryption, logging, and modular Python components to offer a flexible solution for managing tokens in various applications. It includes tools to maintain system integrity and ensures ease of use for developers.

---
## Features
- **Secure Token Generation**:
  - Generates unique, encrypted tokens using the Fernet encryption standard.
  - Ensures tokens cannot be reverse-engineered or tampered with.

- **Token Validation**:
  - Validates token authenticity and checks expiration status.

- **Efficient Database Handling**:
  - SQLite-based database to store tokens with timestamps.
  - Supports token revocation for added security.

- **Utilities**:
  - Purge script to clear logs and database entries.
  - Tool to generate new encryption keys safely.

- **Modular Design**:
  - Separated components for token generation, validation, and management.
  - Easy to extend and integrate with other systems.

---

## Project Structure
```
.env
.gitignore
api.py
bincat_tokens.db
LICENSE
main.py
README.md
requirements.txt
setup.py

.github/
  dependabot.yml

bincat/
  token_generator.py
  token_manager.py
  token_validator.py
  __init__.py

tools/
  encryption_key_gen.py
  purge.py

tests/
  test_bincat.py
  test_token_manager.py
  __init__.py
```

---

## Installation
### Prerequisites
- Python 3.10 or later
- SQLite (built into Python)
- `pip` for package management

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/BinCat.git
   cd BinCat
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Generate an encryption key (if not already generated):
   ```bash
   python tools/encryption_key_gen.py
   ```
   This will create a `.env` file containing the encryption key.

---

## Usage
### Running the Application
Execute the main script:
```bash
python main.py
```

### Available Functionalities
- **Generate Token**: Automatically creates a new secure token.
- **Validate Token**: Checks if a token is valid and not expired.
- **Revoke Token**: Marks a token as revoked to prevent its further use.

### Maintenance Tools
- **Purge Logs and Database**:
  Clear all logs and reset the database:
  ```bash
  python tools/purge.py
  ```
- **Generate New Encryption Key**:
  Create a new encryption key for enhanced security:
  ```bash
  python tools/encryption_key_gen.py
  ```
  > Note: Changing the encryption key will invalidate all existing tokens.

---

## Technologies Used
- **Python**: Core language for development.
- **SQLite**: Lightweight database for token storage.
- **Cryptography**: Secure encryption and decryption.
- **Colorama**: Console color formatting.

---

## Testing
Unit tests are located in the `tests` folder. To run the tests:
```bash
python -m unittest discover -s tests
```

---

## Contributing
Contributions are welcome! Follow these steps to contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a Pull Request.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact
For questions or suggestions, feel free to reach out:
- **GitHub**: [eduolihez](https://github.com/eduolihez)
- **Telegram**: [eduolihez](t.me/eduolihez)

If you found this project helpful, consider giving it a ⭐ on GitHub!

