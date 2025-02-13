import os
import asyncio
from pyrogram import Client, filters
from flask import Flask
import threading

# Load session string from environment variables
SESSION_STRING = os.getenv("PYROGRAM_SESSION_STRING")

# Initialize Pyrogram Client
app = Client("my_account", session_string=SESSION_STRING)

# Initialize Flask app for Render port binding
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Userbot is running!"

# /start command (moved here)
@app.on_message(filters.command("start") & filters.me)
async def start_cmd(client, message):
    await message.reply_text("✅ Userbot is active and running!")

# Ensure commands are properly imported
from commands.gld_img import gld_img_cmd
from commands.gld_vid import gld_vid_cmd

app.add_handler(filters.command("gld_img")(gld_img_cmd))
app.add_handler(filters.command("gld_vid")(gld_vid_cmd))

def run_flask():
    flask_app.run(host="0.0.0.0", port=10000)  # Render requires port binding

async def run_pyrogram():
    print("Starting Pyrogram client...")
    await app.start()
    print("Pyrogram client is running...")
    await asyncio.Event().wait()  # Keeps Pyrogram running

# Start both Flask and Pyrogram together
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    asyncio.run(run_pyrogram())