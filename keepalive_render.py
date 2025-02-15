import os
import threading
from flask import Flask
from waitress import serve  # Production WSGI server

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Userbot is running!"

def run_flask():
    port = int(os.getenv("PORT", "5000"))  # Ensure PORT is set correctly in Render
    serve(flask_app, host="0.0.0.0", port=port)  # Use Waitress instead of Flask's built-in server

# Start Flask in a separate thread to avoid blocking
def start_keepalive():
    thread = threading.Thread(target=run_flask, daemon=True)
    thread.start()