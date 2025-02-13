import os
import asyncio
from flask import Flask
from pyrogram import Client, filters

# Importing commands
from commands.gld_img import gld_img_cmd
from commands.gld_vid import gld_vid_cmd

# Load session string from environment variable
SESSION_STRING = os.getenv("PYROGRAM_SESSION_STRING")

# Initialize Flask for Render port binding
app = Flask(__name__)

@app.route('/')
def home():
    return "Userbot is running!"

# Pyrogram Client
userbot = Client("userbot", session_string=SESSION_STRING)

# ✅ `/start` command to check if the userbot is active
@userbot.on_message(filters.command("start", prefixes=["/", "!"]) & filters.me)
async def start(client, message):
    await message.reply_text("✅ Userbot is active and responding!")

# Registering commands from external files
userbot.add_handler(gld_img_cmd)
userbot.add_handler(gld_vid_cmd)

# Run Pyrogram in async mode
async def run():
    await userbot.start()
    print("Userbot is running...")
    await asyncio.Future()  # Keeps running

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run())
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))