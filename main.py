import os
import logging
import asyncio
import threading
from pyrogram import Client, filters
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

# Flask keep-alive server for Render
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Userbot is running!"

def run_flask():
    port = int(os.getenv("PORT", "5000"))  # Ensure it's 5000 for Render
    flask_app.run(host="0.0.0.0", port=port)

# Start Flask in a separate thread to avoid blocking
threading.Thread(target=run_flask, daemon=True).start()

async def main():
    await app.start()
    print("Userbot is running!")
    
    try:
        await asyncio.Event().wait()  # Keep running indefinitely
    finally:
        await app.stop()
        print("Userbot stopped.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())