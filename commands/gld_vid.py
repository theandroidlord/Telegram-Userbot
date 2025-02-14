import os
import logging
import asyncio
import shlex
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import RetryAfter

DOWNLOAD_DIR = "downloads"

async def fetch_and_send_video(chat_id, file_path, context):
    """Sends a downloaded video to Telegram."""
    try:
        await asyncio.sleep(5)  # Delay to avoid flood limits
        with open(file_path, 'rb') as video_file:
            try:
                await context.bot.send_video(chat_id, video=video_file)
            except RetryAfter as e:
                logging.warning(f"Flood control exceeded. Retrying in {e.retry_after} seconds...")
                await asyncio.sleep(e.retry_after)
                await context.bot.send_video(chat_id, video=video_file)
    except Exception as e:
        logging.error(f"Error sending video: {e}")
    finally:
        os.remove(file_path)


async def gld_vid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Downloads and sends videos using gallery-dl."""
    chat_id = str(update.message.chat_id)

    if not context.args:
        await update.message.reply_text("❌ Please provide a valid URL.")
        return

    url = ' '.join(context.args)
    await update.message.reply_text(f"🔄 Fetching videos from {url}...")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Extract only video URLs
    media_process = await asyncio.create_subprocess_exec(
        *shlex.split(f'gallery-dl --get-urls {url}'),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    media_stdout, _ = await media_process.communicate()
    media_urls = [line.strip() for line in media_stdout.decode().splitlines() if line.strip()]
    video_urls = [url for url in media_urls if url.lower().endswith((".mp4", ".mkv", ".webm"))]

    if not video_urls:
        await update.message.reply_text("❌ No videos found.")
        return

    await update.message.reply_text(f"✅ Found {len(video_urls)} videos. Downloading...")

    for video_url in video_urls:
        process = await asyncio.create_subprocess_exec(
            *shlex.split(f'gallery-dl -d {DOWNLOAD_DIR} {video_url}'),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()

        downloaded_files = os.listdir(DOWNLOAD_DIR)
        video_files = [os.path.join(DOWNLOAD_DIR, f) for f in downloaded_files if f.endswith((".mp4", ".mkv", ".webm"))]

        for file_path in video_files:
            await fetch_and_send_video(chat_id, file_path, context)

    await update.message.reply_text("✅ All available videos sent.")