from flask import Flask, render_template, request, redirect, url_for
from bincat.token_manager import TokenManager
import os

app = Flask(__name__)
token_manager = TokenManager()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_token():
    token = token_manager.generate_token()
    return f"Generated Token: {token}"

@app.route("/logs")
def view_logs():
    if os.path.exists("logs.txt"):
        with open("logs.txt", "r") as f:
            logs = f.readlines()
        return render_template("logs.html", logs=logs)
    return "No logs found!"

if __name__ == "__main__":
    app.run(debug=True)
