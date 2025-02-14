import os
import asyncio
import shlex
from pyrogram import Client, filters
import subprocess

# Initialize Userbot Client
app = Client("my_userbot")

# Ensure download folder exists
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@app.on_message(filters.command("gld_vid") & filters.me)
async def gld_vid_cmd(client, message):
    """Downloads and sends videos from a gallery-dl supported site."""
    if len(message.command) < 2:
        await message.reply("❌ Please provide a URL.")
        return

    media_url = message.command[1]
    await message.reply(f"🔄 Fetching videos from {media_url}...")

    # Get video URLs using gallery-dl
    process = await asyncio.create_subprocess_exec(
        *shlex.split(f'gallery-dl --get-urls {media_url}'),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    video_urls = [line.strip() for line in stdout.decode().splitlines() if line.strip().endswith(".mp4")]

    if not video_urls:
        await message.reply("❌ No video found after fetching links.")
        return

    await message.reply(f"✅ Found {len(video_urls)} videos. Downloading...")

    for video_url in video_urls:
        await message.reply(f"⬇️ Downloading: {video_url}")

        # Download video with gallery-dl
        download_cmd = f'gallery-dl -d {DOWNLOAD_DIR} {video_url}'
        process = subprocess.run(shlex.split(download_cmd), capture_output=True, text=True)

        # Find downloaded file
        files = sorted(os.listdir(DOWNLOAD_DIR), key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_DIR, x)))
        if not files:
            await message.reply(f"❌ Failed to download: {video_url}")
            continue

        file_path = os.path.join(DOWNLOAD_DIR, files[-1])
        await message.reply_video(file_path)

        # Delete file after sending
        os.remove(file_path)
        await asyncio.sleep(5)  # Prevent spam

    await message.reply("✅ All available videos have been sent!")


app.run()