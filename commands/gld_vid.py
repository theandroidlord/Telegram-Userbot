import os
import asyncio
import logging
import subprocess
from pyrogram import Client, filters

async def gld_vid_cmd(client, message):
    if len(message.command) < 2:
        await message.reply_text("❌ Please provide a valid URL.")
        return

    url = message.command[1]
    download_path = "downloads"
    os.makedirs(download_path, exist_ok=True)

    await message.reply_text("⏳ Downloading video...")

    # Run gallery-dl command to download video
    try:
        command = ["gallery-dl", "-d", download_path, url]
        process = await asyncio.create_subprocess_exec(*command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            logging.error(f"Download error: {stderr.decode().strip()}")
            await message.reply_text("❌ Failed to download video.")
            return

    except Exception as e:
        logging.error(f"Error downloading video: {str(e)}")
        await message.reply_text("❌ An error occurred while downloading.")
        return

    # Find the downloaded video file
    video_files = [f for f in os.listdir(download_path) if f.endswith((".mp4", ".mkv", ".webm"))]

    if not video_files:
        await message.reply_text("❌ No video found after download.")
        return

    video_path = os.path.join(download_path, video_files[0])

    await message.reply_text("📤 Uploading video...")

    try:
        await client.send_video(
            chat_id=message.chat.id,
            video=video_path,
            caption=""
        )
        await message.reply_text("✅ Video uploaded successfully!")

        # Clean up file after upload
        os.remove(video_path)

    except Exception as e:
        logging.error(f"Error uploading video: {str(e)}")
        await message.reply_text("❌ Failed to upload video.")