import os
import logging
import asyncio
import yt_dlp
import aiohttp
import shlex
from dotenv import load_dotenv
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ALLOWED_CHAT_IDS = os.getenv('ALLOWED_CHAT_IDS', "").split(',')

# Set up logging
logging.basicConfig(level=logging.INFO)

# Flask app for Render port binding fix
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responds to /start command."""
    await update.message.reply_text("Send a YouTube Shorts link, and I'll download it!")

async def download_youtube_video(url):
    """Downloads a YouTube Shorts video using yt-dlp."""
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "b[ext=mp4]",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "quiet": True,
        "no_warnings": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename
    except Exception as e:
        logging.error(f"yt-dlp error: {e}")
        return None

async def handle_youtube_shorts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Detects YouTube Shorts links and downloads the video."""
    url = update.message.text.strip()

    if "youtube.com/shorts/" not in url and "youtu.be/" not in url:
        return  # Ignore non-Shorts links

    await update.message.reply_text("Downloading Shorts video...")

    video_path = await download_youtube_video(url)

    if video_path and os.path.exists(video_path):
        await update.message.reply_video(video=open(video_path, "rb"))
        os.remove(video_path)  # Clean up after sending
    else:
        await update.message.reply_text("Download failed.")

def main() -> None:
    """Start the bot using polling."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & filters.Entity("url"), handle_youtube_shorts))

    # Run bot in an asyncio event loop
    loop = asyncio.get_event_loop()
    loop.create_task(application.run_polling())

    # Start Flask app on port 8080
    app.run(host="0.0.0.0", port=8080)

if __name__ == '__main__':
    main()