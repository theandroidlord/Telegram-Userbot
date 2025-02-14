import asyncio
import shlex
import os
from pyrogram import Client

DOWNLOAD_DIR = "downloads"

async def gld_vid_cmd(client: Client, message):
    if len(message.command) < 2:
        await message.reply_text("❌ Please provide a URL.")
        return

    url = message.command[1]
    await message.reply_text(f"🔄 Downloading videos from {url}...")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Run gallery-dl to download directly
    process = await asyncio.create_subprocess_exec(
        *shlex.split(f'gallery-dl -d {DOWNLOAD_DIR} {url}'),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    logging_output = stdout.decode() + stderr.decode()
    print(logging_output)  # Debugging

    # Check for downloaded videos
    video_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith((".mp4", ".mkv", ".webm"))]

    if not video_files:
        await message.reply_text("❌ No video found after download.")
        return

    await message.reply_text(f"✅ Found {len(video_files)} videos. Sending...")

    for vid_file in video_files:
        vid_path = os.path.join(DOWNLOAD_DIR, vid_file)

        try:
            await message.reply_video(vid_path)
        except Exception as e:
            await message.reply_text(f"⚠️ Failed to send {vid_file}: {e}")
        
        os.remove(vid_path)  # Delete after sending
        await asyncio.sleep(5)  # Avoid rate limit

    await message.reply_text("✅ All videos sent.")

__all__ = ["gld_vid_cmd"]