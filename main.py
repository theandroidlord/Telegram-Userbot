import os
import logging
import asyncio
import shlex
import re
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Regex to detect YouTube Shorts links
YOUTUBE_SHORTS_REGEX = re.compile(r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/shorts\/|youtu\.be\/)([\w\-]+)")

async def download_video(url: str) -> str:
    """Downloads a YouTube Shorts video using yt-dlp."""
    os.makedirs("downloads", exist_ok=True)
    
    output_template = "downloads/video.%(ext)s"
    command = f'yt-dlp -o "{output_template}" {shlex.quote(url)}'
    logger.info(f"Running: {command}")

    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        # Find the actual downloaded file (since it could have any extension)
        for file in os.listdir("downloads"):
            if file.startswith("video.") and not file.endswith(".mp4"):
                return os.path.join("downloads", file)
    else:
        logger.error(f"yt-dlp failed: {stderr.decode()}")
    
    return None

async def convert_to_mp4(input_file: str) -> str:
    """Converts the video to 1080p MP4 using ffmpeg."""
    output_file = "downloads/converted.mp4"
    command = f'ffmpeg -i "{input_file}" -vf "scale=-1:1080" -c:v libx264 -preset fast -c:a aac "{output_file}" -y'
    
    logger.info(f"Running: {command}")
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        return output_file
    else:
        logger.error(f"FFmpeg conversion failed: {stderr.decode()}")
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Detects YouTube Shorts links and downloads the video."""
    if update.message and update.message.text:
        match = YOUTUBE_SHORTS_REGEX.search(update.message.text)
        if match:
            url = update.message.text.strip()
            await update.message.reply_text("Downloading video...")

            downloaded_file = await download_video(url)
            if downloaded_file:
                converted_file = await convert_to_mp4(downloaded_file)
                os.remove(downloaded_file)  # Remove the original downloaded file

                if converted_file:
                    await update.message.reply_video(video=open(converted_file, "rb"))
                    os.remove(converted_file)  # Remove converted file after sending
                else:
                    await update.message.reply_text("Conversion failed.")
            else:
                await update.message.reply_text("Download failed.")

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == '__main__':
    main()