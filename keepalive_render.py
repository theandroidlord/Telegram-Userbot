import os
import threading
from flask import Flask
# Flask Server To Keep Render Free Account Active 24/7 
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Userbot is running!"

def run_flask():
    port = int(os.getenv("PORT", "5000"))  # Ensure it's 5000 for Render
    flask_app.run(host="0.0.0.0", port=port)

# Start Flask in a separate thread to avoid blocking
def start_keepalive():
    thread = threading.Thread(target=run_flask, daemon=True)
    thread.start()