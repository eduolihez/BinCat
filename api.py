from flask import Flask, request, jsonify
from bincat.token_manager import TokenManager

app = Flask(__name__)
manager = TokenManager()

@app.route('/generate', methods=['POST'])
def generate():
    token = manager.generate_token()
    return jsonify({"token": token})

@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    token = data.get("token")
    if not token:
        return jsonify({"error": "Token is required"}), 400
    is_valid = manager.is_token_valid(token)
    return jsonify({"valid": is_valid})

@app.route('/revoke', methods=['POST'])
def revoke():
    data = request.json
    token = data.get("token")
    if not token:
        return jsonify({"error": "Token is required"}), 400
    revoked = manager.revoke_token(token)
    return jsonify({"revoked": revoked})

@app.route('/tokens', methods=['GET'])
def list_tokens():
    tokens = manager.list_active_tokens()
    return jsonify({"active_tokens": tokens})

if __name__ == '__main__':
    app.run(debug=True)
