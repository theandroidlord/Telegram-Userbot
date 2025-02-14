import os
import logging
import asyncio
import shlex
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import RetryAfter

DOWNLOAD_DIR = "downloads"

async def fetch_and_send_image(chat_id, file_path, context):
    """Sends a downloaded image to Telegram."""
    try:
        await asyncio.sleep(5)  # Delay to avoid flood limits
        with open(file_path, 'rb') as img_file:
            try:
                await context.bot.send_photo(chat_id, photo=img_file)
            except RetryAfter as e:
                logging.warning(f"Flood control exceeded. Retrying in {e.retry_after} seconds...")
                await asyncio.sleep(e.retry_after)
                await context.bot.send_photo(chat_id, photo=img_file)
    except Exception as e:
        logging.error(f"Error sending image: {e}")
    finally:
        os.remove(file_path)


async def gld_img(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Downloads and sends images using gallery-dl."""
    chat_id = str(update.message.chat_id)

    if not context.args:
        await update.message.reply_text("❌ Please provide a valid URL.")
        return

    url = ' '.join(context.args)
    await update.message.reply_text(f"🔄 Fetching images from {url}...")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Extract only image URLs
    media_process = await asyncio.create_subprocess_exec(
        *shlex.split(f'gallery-dl --get-urls {url}'),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    media_stdout, _ = await media_process.communicate()
    media_urls = [line.strip() for line in media_stdout.decode().splitlines() if line.strip()]
    image_urls = [url for url in media_urls if url.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))]

    if not image_urls:
        await update.message.reply_text("❌ No images found.")
        return

    await update.message.reply_text(f"✅ Found {len(image_urls)} images. Downloading...")

    for image_url in image_urls:
        process = await asyncio.create_subprocess_exec(
            *shlex.split(f'gallery-dl -d {DOWNLOAD_DIR} {image_url}'),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()

        downloaded_files = os.listdir(DOWNLOAD_DIR)
        image_files = [os.path.join(DOWNLOAD_DIR, f) for f in downloaded_files if f.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))]

        for file_path in image_files:
            await fetch_and_send_image(chat_id, file_path, context)

    await update.message.reply_text("✅ All available images sent.")