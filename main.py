import os
import re
import shlex
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Regex to detect YouTube Shorts links
YOUTUBE_SHORTS_REGEX = re.compile(r"(https?://)?(www\.)?(youtube\.com/shorts/|youtu\.be/)([\w-]+)")

async def download_and_send_youtube_shorts(video_url: str, chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    """Download YouTube Shorts using Piped and send to Telegram."""
    match = YOUTUBE_SHORTS_REGEX.search(video_url)
    if not match:
        logging.error("Invalid YouTube Shorts URL.")
        return

    video_id = match.group(4)  # Extract video ID
    piped_url = f"https://piped.video/{video_id}"
    output_file = f"downloads/{video_id}.mp4"

    os.makedirs("downloads", exist_ok=True)

    try:
        # Download video from Piped using yt-dlp
        process = await asyncio.create_subprocess_exec(
            *shlex.split(f"yt-dlp -o '{output_file}' {piped_url}"),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            logging.error(f"yt-dlp failed: {stderr.decode()}")
            return

        # Convert to MP4 if needed using FFmpeg
        final_file = f"downloads/{video_id}_final.mp4"
        convert_process = await asyncio.create_subprocess_exec(
            "ffmpeg", "-i", output_file, "-c:v", "libx264", "-preset", "fast", "-crf", "23", "-c:a", "aac", "-b:a", "128k", final_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await convert_process.communicate()

        if os.path.exists(final_file):
            await context.bot.send_video(chat_id, video=open(final_file, "rb"))
            os.remove(final_file)
        else:
            await context.bot.send_video(chat_id, video=open(output_file, "rb"))

        os.remove(output_file)  # Cleanup original file
    except Exception as e:
        logging.error(f"Download error: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Detect Shorts links and process them."""
    message_text = update.message.text
    chat_id = update.message.chat_id

    if YOUTUBE_SHORTS_REGEX.search(message_text):
        await update.message.reply_text("Downloading YouTube Shorts...")
        await download_and_send_youtube_shorts(message_text, chat_id, context)

def main():
    """Start the bot using polling."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add a message handler to detect YouTube Shorts links
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()