import os
import re
import shlex
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Regex pattern for detecting YouTube Shorts links
YT_SHORTS_PATTERN = re.compile(r"(https?://)?(www\.)?(youtube\.com/shorts/|youtu\.be/)")

async def download_and_convert(video_url: str) -> str:
    """Downloads video using yt-dlp and converts to MP4 using ffmpeg."""
    os.makedirs("downloads", exist_ok=True)
    temp_file = "downloads/temp_video"
    output_file = "downloads/output.mp4"

    # Step 1: Download video naturally
    download_cmd = f'yt-dlp -o "{temp_file}" {video_url}'
    process = await asyncio.create_subprocess_shell(download_cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    await process.communicate()

    if process.returncode != 0:
        logger.error("yt-dlp download failed.")
        return None

    # Step 2: Convert to MP4 using ffmpeg
    convert_cmd = f'ffmpeg -y -i "{temp_file}" -c:v libx264 -preset fast -c:a aac "{output_file}"'
    process = await asyncio.create_subprocess_shell(convert_cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    await process.communicate()

    if process.returncode != 0:
        logger.error("FFmpeg conversion failed.")
        return None

    return output_file

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Detects YouTube Shorts links and processes them."""
    message = update.message.text
    if not message:
        return

    match = YT_SHORTS_PATTERN.search(message)
    if match:
        video_url = match.group(0)
        chat_id = update.message.chat_id

        await update.message.reply_text(f"Downloading: {video_url}")
        video_path = await download_and_convert(video_url)

        if video_path:
            await context.bot.send_video(chat_id, video=open(video_path, "rb"))
            os.remove(video_path)
        else:
            await update.message.reply_text("Download failed.")

def main():
    """Starts the Telegram bot with polling."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Handle messages with YouTube Shorts links
    application.add_handler(MessageHandler(filters.TEXT & filters.Entity("url"), handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()