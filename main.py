import os
import logging
import asyncio
import threading
from pyrogram import Client
from flask import Flask

# Load environment variables
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
SESSION_STRING = os.getenv("PYROGRAM_SESSION_STRING", "")

if not SESSION_STRING:
    raise ValueError("PYROGRAM_SESSION_STRING is missing from environment variables!")

# Initialize Pyrogram client
app = Client("userbot", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

# Import & register commands
from commands.weather_command import register_weather_command  
register_weather_command(app)

# Flask server for Render keep-alive
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return "Alive"

def run_flask():
    flask_app.run(host="0.0.0.0", port=10000, threaded=True)

async def start_services():
    """Start Flask server and Userbot"""
    threading.Thread(target=run_flask, daemon=True).start()  # Run Flask in a separate thread
    await app.start()
    print("Userbot is running!")
    await asyncio.Event().wait()  # Keep bot running

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Run main bot process
    asyncio.run(start_services())