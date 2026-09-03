# BinCat

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Dashboard-000000.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

### **[Versión en Español](README.md)** · [English version](README.en.md)

BinCat genera, valida y revoca tokens de autenticación, y deja registro de cada
operación. Se distribuye como un SDK de Python que puedes meter en tu
aplicación, con un panel web y una API REST encima.

## Funcionalidades

Emite dos tipos de token: Fernet, con criptografía simétrica, y JWT firmados
criptográficamente con claims con estado. Los intervalos de expiración se
configuran desde el slider del panel o desde la API, y cualquier token se puede
revocar a mano para matar una sesión al instante.

El panel es una página única de tema oscuro donde generas, validas y revocas
tokens. Muestra el recuento de tokens totales, activos, revocados y expirados, y
una consola de logs que traza las acciones del SDK según ocurren.

No hay nada que configurar antes del primer arranque. Si BinCat no encuentra
claves en `.env`, genera unas criptográficamente seguras.

## Estructura del proyecto

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

## Instalación

Necesitas Python 3.10 o superior y `pip`.

1. Clona el repositorio y entra en la carpeta:
   ```bash
   git clone https://github.com/eduolihez/BinCat.git
   cd BinCat
   ```

2. (Opcional) Monta un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Arranca el servidor de desarrollo de Flask y abre `http://localhost:5000` para
el panel:

```bash
python app.py
```

También hay una interfaz de terminal, si prefieres no salir de la shell:

```bash
python main.py
```

## Endpoints de la API REST

Manda todos los payloads como `application/json`.

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/tokens` | Devuelve la lista de tokens con sus metadatos (estado, tipo, creación, duración). |
| POST | `/api/tokens/generate` | Genera un token. Cuerpo: `{"token_type": "fernet\|jwt", "expiration_minutes": 30, "description": "text"}`. |
| POST | `/api/tokens/validate` | Comprueba si un token es válido. Cuerpo: `{"token": "token_string"}`. |
| POST | `/api/tokens/revoke` | Revoca un token al momento. Cuerpo: `{"token": "token_string"}`. |
| POST | `/api/tokens/purge` | Borra permanentemente las entradas de la base de datos y los archivos de log. |
| GET | `/api/logs` | Devuelve las últimas 50 entradas del log de actividad. |

## Tests

Los tests corren contra una base de datos SQLite aislada, así que no tocan la de
desarrollo:

```bash
python -m unittest discover -s tests
```

## Seguridad

`.env` contiene la `ENCRYPTION_KEY` que cifra todos los tokens Fernet de tu base
de datos. BinCat la genera en el primer arranque y el `.gitignore` ya la cubre.
No subas nunca tu `.env` real; usa `.env.example` como plantilla. Si una clave se
filtra, borra `.env` y deja que BinCat genere otra, y luego reemite los tokens
que estaban cifrados con la anterior.

## Licencia

MIT. Ver el archivo `LICENSE`.
