import os
import asyncio
import shlex
import logging
from pyrogram import Client, filters

# Load string session from environment
STRING_SESSION = os.getenv("PYROGRAM_STRING_SESSION")  # Using string session only

# Initialize Pyrogram Client
app = Client("userbot", session_string=STRING_SESSION)

# Set up logging
logging.basicConfig(level=logging.INFO)

async def fetch_and_send_media(client, message, media_type):
    """Extracts and downloads media using gallery-dl, then sends it to Telegram."""
    if len(message.command) < 2:
        await message.reply_text("❌ Please provide a valid URL.")
        return
    
    media_url = message.command[1]
    await message.reply_text(f"🔄 Fetching {media_type}s from {media_url}...")

    # Get all media links
    process = await asyncio.create_subprocess_exec(
        *shlex.split(f'gallery-dl --get-urls {media_url}'),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, _ = await process.communicate()
    media_urls = [url.strip() for url in stdout.decode().splitlines() if url.strip()]

    # Filter based on command
    if media_type == "video":
        filtered_urls = [url for url in media_urls if url.lower().endswith((".mp4", ".mov", ".avi", ".mkv"))]
    else:
        filtered_urls = [url for url in media_urls if url.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))]

    if not filtered_urls:
        await message.reply_text(f"❌ No {media_type}s found.")
        return

    await message.reply_text(f"✅ Found {len(filtered_urls)} {media_type}(s). Downloading...")

    for media_link in filtered_urls:
        try:
            # Download using gallery-dl
            process = await asyncio.create_subprocess_exec(
                *shlex.split(f'gallery-dl -d downloads {media_link}'),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()

            # Find the downloaded file
            downloaded_files = [f for f in os.listdir("downloads") if f.endswith(media_link[-4:])]
            if not downloaded_files:
                await message.reply_text(f"❌ Failed to download: {media_link}")
                continue

            file_path = os.path.join("downloads", downloaded_files[0])

            # Send media to Telegram
            await asyncio.sleep(5)  # Avoid flood limits
            if media_type == "video":
                await client.send_video(message.chat.id, file_path)
            else:
                await client.send_photo(message.chat.id, file_path)

            # Remove the file after sending
            os.remove(file_path)

        except Exception as e:
            logging.error(f"Error processing {media_link}: {e}")
            await message.reply_text(f"❌ Error processing media: {media_link}")

    await message.reply_text("✅ All available media sent.")

# Handle both /gld_img and /gld_vid
@app.on_message(filters.command(["gld_img", "gld_vid"]) & filters.me)
async def handle_gallery_dl(client, message):
    """Handles /gld_img and /gld_vid commands."""
    media_type = "image" if message.command[0] == "gld_img" else "video"
    await fetch_and_send_media(client, message, media_type)

# Start the userbot
app.run()