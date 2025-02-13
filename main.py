import os
import asyncio
import threading
from pyrogram import Client, filters
from flask import Flask

# Load session string from environment variables
SESSION_STRING = os.getenv("PYROGRAM_SESSION_STRING")

# Initialize Pyrogram Client
app = Client("my_account", session_string=SESSION_STRING)

# Initialize Flask for Render port binding
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Userbot is running!"

# Import commands (Using Import Method)
from commands.gld_img import gld_img_cmd
from commands.gld_vid import gld_vid_cmd
# Import start command

# Function to run Flask for Render
def run_flask():
    flask_app.run(host="0.0.0.0", port=10000)

# Function to run Pyrogram
async def run_pyrogram():
    print("Starting Pyrogram client...")
    await app.start()
    print("Pyrogram client is running...")
    await asyncio.Event().wait()

# Start both Flask and Pyrogram
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    asyncio.run(run_pyrogram())