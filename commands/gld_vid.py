import os
import shlex
import asyncio
from pyrogram import Client, filters

async def download_video(url):
    """Downloads only video files using gallery-dl."""
    os.makedirs("downloads", exist_ok=True)
    
    process = await asyncio.create_subprocess_exec(
        *shlex.split(f'gallery-dl -d downloads {url}'),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()
    
    downloaded_files = os.listdir("downloads")
    video_files = [file for file in downloaded_files if file.lower().endswith((".mp4", ".webm", ".mkv", ".mov"))]

    return video_files

async def gld_vid_cmd(client, message):
    """Handles the /gld_vid command to download videos only."""
    if len(message.command) < 2:
        await message.reply_text("Usage: `/gld_vid <URL>`")
        return

    url = message.command[1]
    await message.reply_text(f"Downloading videos from: {url}")

    video_files = await download_video(url)

    if not video_files:
        await message.reply_text("❌ No video found after download.")
        return

    for video_file in video_files:
        video_path = os.path.join("downloads", video_file)
        await client.send_video(message.chat.id, video=video_path)
        os.remove(video_path)

    await message.reply_text("✅ All videos sent.")