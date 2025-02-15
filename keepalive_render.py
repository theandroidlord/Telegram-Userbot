from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Userbot is running!"

def start_keepalive():
    """Starts the Flask keep-alive server on Render."""
    port = int(os.getenv("PORT", 10000))  # Render uses dynamic port binding
    app.run(host="0.0.0.0", port=port, threaded=True)