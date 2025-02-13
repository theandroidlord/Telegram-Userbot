import os
import subprocess
from pyrogram import Client, filters

@Client.on_message(filters.command("gld_img") & filters.me)
async def gld_img(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /gld_img <URL>")
        return

    url = message.command[1]
    await message.reply_text(f"Downloading images from {url}...")

    # Run gallery-dl command to download images only
    process = subprocess.run(
        ["gallery-dl", "-f", "jpg,png,gif", url], 
        capture_output=True, text=True
    )

    if process.returncode == 0:
        await message.reply_text("Images downloaded successfully!")
    else:
        await message.reply_text("Failed to download images.")