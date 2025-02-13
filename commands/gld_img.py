import os
import subprocess
from pyrogram import Client, filters

async def gld_img(client, message):
    url = message.text.split(" ", 1)[1] if len(message.command) > 1 else None
    if not url:
        await message.reply_text("Usage: /gld_img <URL>")
        return
    
    await message.reply_text("Downloading images...")
    subprocess.run(["gallery-dl", "-q", "--filter", "ext in ('jpg', 'png', 'jpeg')", url])
    await message.reply_text("Download complete!")

gld_img_cmd = filters.command("gld_img", prefixes=["/", "!"]) & filters.me