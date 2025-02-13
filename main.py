import os
import logging
from pyrogram import Client, filters
from commands.gld_img import gld_img_cmd
from commands.gld_vid import gld_vid_cmd

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Load session string from environment variable
SESSION_STRING = os.getenv("PYROGRAM_SESSION_STRING")

# Initialize Pyrogram client
app = Client("my_account", session_string=SESSION_STRING)

# Start command
@app.on_message(filters.command("start") & filters.me)
async def start_cmd(client, message):
    await message.reply_text("Userbot is Active!")

# /gld_img command
@app.on_message(filters.command("gld_img") & filters.me)
async def gld_img_handler(client, message):
    await gld_img_cmd(client, message)

# /gld_vid command
@app.on_message(filters.command("gld_vid") & filters.me)
async def gld_vid_handler(client, message):
    await gld_vid_cmd(client, message)

# Debugging: Check if userbot is receiving messages
@app.on_message(filters.text & filters.me)
async def debug_message(client, message):
    logging.debug(f"Received message: {message.text}")

# Start the bot
print("Userbot is running...")
app.run()