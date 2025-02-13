import os
from pyrogram import Client, filters
from commands.gld_vid import gld_vid_cmd
from commands.gld_img import gld_img_cmd

# Load session string from environment variable
SESSION_STRING = os.getenv("PYROGRAM_SESSION_STRING")

# Initialize Pyrogram Client
app = Client("my_account", session_string=SESSION_STRING)

@app.on_message(filters.command("start") & filters.me)
async def start_cmd(client, message):
    await message.reply_text("✅ Userbot is active!\nUse `/gld_img <URL>` or `/gld_vid <URL>`.")

@app.on_message(filters.command("gld_vid") & filters.me)
async def gld_vid_handler(client, message):
    await gld_vid_cmd(client, message)

@app.on_message(filters.command("gld_img") & filters.me)
async def gld_img_handler(client, message):
    await gld_img_cmd(client, message)

print("Userbot is running...")
app.run()