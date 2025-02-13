import subprocess
from pyrogram import Client, filters

async def gld_vid_cmd(client: Client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a URL.")
        return
    
    url = message.command[1]
    await message.reply_text("Downloading video...")

    process = subprocess.run(["gallery-dl", "-f", "mp4,mkv", url], capture_output=True, text=True)

    if process.returncode == 0:
        await message.reply_text("Video downloaded successfully!")
    else:
        await message.reply_text(f"Download failed. Error: {process.stderr}")