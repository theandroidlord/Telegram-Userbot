import os
import logging
import asyncio
import threading
from flask import Flask
from pyrogram import Client, filters

# Load environment variables
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
SESSION_STRING = os.getenv("PYROGRAM_SESSION_STRING", "")

if not SESSION_STRING:
    raise ValueError("PYROGRAM_SESSION_STRING is missing from environment variables!")

# Initialize Pyrogram client
app = Client("userbot", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

# Flask server for keeping Render service alive
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Userbot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port, threaded=True)

# Start Flask in a separate thread
threading.Thread(target=run_flask, daemon=True).start()

# Debug: Log every 2 seconds to confirm Pyrogram is running
async def debug_log():
    while True:
        print("Pyrogram: OK")
        await asyncio.sleep(2)

# Import & register commands
from commands.weather_command import register_weather_command
register_weather_command(app)

# Basic message handler for debugging
@app.on_message(filters.text & filters.private)
async def debug_messages(client, message):
    print(f"Received message from {message.chat.id}: {message.text}")
    await message.reply("I am alive!")

async def main():
    await app.start()
    print("Userbot is running!")
    asyncio.create_task(debug_log())  # Start debug logging
    await asyncio.Event().wait()  # Keep running indefinitely

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())