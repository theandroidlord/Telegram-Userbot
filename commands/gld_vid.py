import os
import subprocess
from pyrogram import Client, filters

@Client.on_message(filters.command("gld_vid") & filters.me)
async def gld_vid(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /gld_vid <URL>")
        return

    url = message.command[1]
    await message.reply_text(f"Downloading video from {url}...")

    # Run gallery-dl command to download videos only
    process = subprocess.run(
        ["gallery-dl", "-f", "mp4,webm,mkv", url], 
        capture_output=True, text=True
    )

    if process.returncode == 0:
        await message.reply_text("Video downloaded successfully!")
    else:
        await message.reply_text("Failed to download video.")