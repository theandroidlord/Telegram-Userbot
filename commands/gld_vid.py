import asyncio
import os
from pyrogram import Client, filters
import subprocess
import glob

DOWNLOAD_PATH = "downloads/"

async def download_videos(url):
    try:
        process = await asyncio.create_subprocess_exec(
            "gallery-dl", "--skip-metadata", "-f", "mp4", "-d", DOWNLOAD_PATH, url,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            print(f"gallery-dl error: {stderr.decode()}")
            return None

        video_files = glob.glob(os.path.join(DOWNLOAD_PATH, "*.mp4"))
        return video_files if video_files else None
    except Exception as e:
        print(f"Error: {e}")
        return None

@Client.on_message(filters.command("gld_vid", prefixes=["/", "!"]) & filters.me)
async def gld_vid_cmd(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: `/gld_vid <URL>`")
        return

    url = message.command[1]
    await message.reply_text("📥 Downloading video...")

    video_files = await download_videos(url)
    
    if not video_files:
        await message.reply_text("❌ Failed to download video.")
        return

    for video in video_files:
        await message.reply_video(video)
        os.remove(video)  # Delete after sending

    await message.reply_text("✅ Video sent successfully!")