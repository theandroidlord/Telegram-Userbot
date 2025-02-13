import os
import asyncio
from flask import Flask
from pyrogram import Client

# Load session string from environment variable
SESSION_STRING = os.getenv("PYROGRAM_SESSION_STRING")

# Initialize Flask for Render port binding
app = Flask(__name__)

@app.route('/')
def home():
    return "Userbot is running!"

# Pyrogram Client
userbot = Client("userbot", session_string=SESSION_STRING)

# Import commands from the `commands` folder
from commands import start, gld_img, gld_vid

# Run Pyrogram in async mode
async def run():
    await userbot.start()
    print("Userbot is running...")
    await asyncio.Future()  # Keeps running

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run())
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))