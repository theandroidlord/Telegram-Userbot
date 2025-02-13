import os
import subprocess
from pyrogram import Client, filters

async def gld_img_cmd(client: Client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a URL.")
        return
    
    url = message.command[1]
    await message.reply_text("Downloading images...")

    # Run gallery-dl to download only images
    process = subprocess.run(["gallery-dl", "-f", "jpg,png", url], capture_output=True, text=True)

    if process.returncode == 0:
        await message.reply_text("Images downloaded successfully!")
    else:
        await message.reply_text("Download failed. Check logs.")