import os
import asyncio
import shlex
from pyrogram import Client, filters
import subprocess

# Initialize Userbot Client
app = Client("my_userbot")

# Ensure download folder exists
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@app.on_message(filters.command("gld_img") & filters.me)
async def gld_img_cmd(client, message):
    """Downloads and sends images from a gallery-dl supported site."""
    if len(message.command) < 2:
        await message.reply("❌ Please provide a URL.")
        return

    media_url = message.command[1]
    await message.reply(f"🔄 Fetching images from {media_url}...")

    # Get image URLs using gallery-dl
    process = await asyncio.create_subprocess_exec(
        *shlex.split(f'gallery-dl --get-urls {media_url}'),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    image_urls = [line.strip() for line in stdout.decode().splitlines() if line.strip().endswith((".jpg", ".png", ".jpeg", ".gif", ".webp"))]

    if not image_urls:
        await message.reply("❌ No images found after fetching links.")
        return

    await message.reply(f"✅ Found {len(image_urls)} images. Downloading...")

    for image_url in image_urls:
        await message.reply(f"⬇️ Downloading: {image_url}")

        # Download image with gallery-dl
        download_cmd = f'gallery-dl -d {DOWNLOAD_DIR} {image_url}'
        process = subprocess.run(shlex.split(download_cmd), capture_output=True, text=True)

        # Find downloaded file
        files = sorted(os.listdir(DOWNLOAD_DIR), key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_DIR, x)))
        if not files:
            await message.reply(f"❌ Failed to download: {image_url}")
            continue

        file_path = os.path.join(DOWNLOAD_DIR, files[-1])
        await message.reply_document(file_path)  # Sends as a file

        # Delete file after sending
        os.remove(file_path)
        await asyncio.sleep(5)  # Prevent spam

    await message.reply("✅ All available images have been sent!")


app.run()