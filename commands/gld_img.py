import asyncio
import shlex
import os
from pyrogram import Client, filters

async def gld_vid_cmd(client: Client, message):
    if len(message.command) < 2:
        await message.reply_text("❌ Please provide a URL.")
        return

    url = message.command[1]
    await message.reply_text(f"🔄 Fetching videos from {url}...")

    # Get media download links
    process = await asyncio.create_subprocess_exec(
        *shlex.split(f'gallery-dl --get-urls {url}'),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, _ = await process.communicate()
    media_urls = stdout.decode().splitlines()

    # Filter only videos
    video_urls = [link for link in media_urls if link.lower().endswith((".mp4", ".mkv", ".webm"))]

    if not video_urls:
        await message.reply_text("❌ No videos found.")
        return

    await message.reply_text(f"✅ Found {len(video_urls)} videos. Downloading...")

    # Process each video one by one
    for vid_url in video_urls:
        vid_process = await asyncio.create_subprocess_exec(
            *shlex.split(f'gallery-dl {vid_url}'),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await vid_process.communicate()

        # Find downloaded file
        downloaded_files = [f for f in os.listdir() if f.endswith((".mp4", ".mkv", ".webm"))]
        if not downloaded_files:
            await message.reply_text("❌ No video found after download.")
            continue

        # Send each video and delete it
        for vid_file in downloaded_files:
            try:
                await message.reply_video(vid_file)
            except Exception as e:
                await message.reply_text(f"⚠️ Failed to send {vid_file}: {e}")
            os.remove(vid_file)  # Delete after sending
            await asyncio.sleep(5)  # 5-second delay between files

    await message.reply_text("✅ All videos sent.")