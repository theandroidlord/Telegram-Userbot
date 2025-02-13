import os
import logging
import asyncio
import shlex
from dotenv import load_dotenv
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Set up logging
logging.basicConfig(level=logging.INFO)

# Flask app for Render port binding
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responds to /start command."""
    await update.message.reply_text("Send a YouTube Shorts link, and I'll download it in 720p!")

async def download_youtube_shorts(url):
    """Downloads a YouTube Shorts video in 720p using yt-dlp."""
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    command = f'yt-dlp -f "best[height=720]" -o "{output_dir}/%(title)s.%(ext)s" {shlex.quote(url)}'
    
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()
    
    if process.returncode != 0:
        logging.error(f"yt-dlp error: {stderr.decode().strip()}")
        return None

    # Find the downloaded file
    files = os.listdir(output_dir)
    if not files:
        return None

    return os.path.join(output_dir, files[0])

async def handle_youtube_shorts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Detects YouTube Shorts links and downloads the video in 720p."""
    url = update.message.text.strip()

    if "youtube.com/shorts/" not in url and "youtu.be/" not in url:
        return  # Ignore non-Shorts links

    await update.message.reply_text("Downloading Shorts video in 720p...")

    video_path = await download_youtube_shorts(url)

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