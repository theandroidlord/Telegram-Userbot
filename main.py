import os
import logging
import yt_dlp
import re
import asyncio
from flask import Flask
from threading import Thread
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app for Render port binding fix
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running."

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# YouTube Shorts URL pattern
YOUTUBE_SHORTS_REGEX = r"(https?:\/\/(?:www\.)?youtube\.com\/shorts\/[a-zA-Z0-9_-]+)"

async def download_youtube_shorts(url):
    """Downloads a YouTube Shorts video using yt-dlp."""
    os.makedirs("downloads", exist_ok=True)
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info_dict)
        return file_path.replace('.webm', '.mp4')  # Ensure mp4 extension

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Checks for YouTube Shorts links and downloads them."""
    message = update.message.text
    chat_id = update.message.chat_id

    shorts_links = re.findall(YOUTUBE_SHORTS_REGEX, message)

    if shorts_links:
        for url in shorts_links:
            await update.message.reply_text(f"Downloading: {url}")
            try:
                file_path = await asyncio.to_thread(download_youtube_shorts, url)
                with open(file_path, 'rb') as video_file:
                    await context.bot.send_video(chat_id, video=video_file)
                os.remove(file_path)
            except Exception as e:
                logging.error(f"Download error: {e}")
                await update.message.reply_text("Failed to download.")

def main():
    """Starts the bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_message))

    # Start Flask server in a separate thread
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()

    application.run_polling()

if __name__ == '__main__':
    main()