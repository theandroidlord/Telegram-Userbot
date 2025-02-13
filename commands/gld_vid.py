import os
import subprocess
from pyrogram import Client, filters

async def gld_vid(client, message):
    url = message.text.split(" ", 1)[1] if len(message.command) > 1 else None
    if not url:
        await message.reply_text("Usage: /gld_vid <URL>")
        return

    await message.reply_text("Downloading videos...")
    subprocess.run(["gallery-dl", "-q", "--filter", "ext in ('mp4', 'webm', 'mkv')", url])
    await message.reply_text("Download complete!")

gld_vid_cmd = filters.command("gld_vid", prefixes=["/", "!"]) & filters.me