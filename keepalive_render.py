from flask import Flask
import threading
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Userbot is running!"

def run():
    """Starts the Flask server on a separate thread to prevent blocking the main bot process."""
    port = int(os.getenv("PORT", 10000))  # Render uses dynamic port binding
    app.run(host="0.0.0.0", port=port, threaded=True)

def start_keepalive():
    """Starts Flask in a separate thread."""
    server_thread = threading.Thread(target=run, daemon=True)
    server_thread.start()