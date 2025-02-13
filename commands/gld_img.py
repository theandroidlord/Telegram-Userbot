import os
import shlex
import asyncio
from pyrogram import Client, filters

async def download_images(url):
    """Downloads only image files using gallery-dl."""
    os.makedirs("downloads", exist_ok=True)
    
    process = await asyncio.create_subprocess_exec(
        *shlex.split(f'gallery-dl -d downloads {url}'),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()

    downloaded_files = os.listdir("downloads")
    image_files = [file for file in downloaded_files if file.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))]

    return image_files

async def gld_img_cmd(client, message):
    """Handles the /gld_img command to download images only."""
    if len(message.command) < 2:
        await message.reply_text("Usage: `/gld_img <URL>`")
        return

    url = message.command[1]
    await message.reply_text(f"Downloading images from: {url}")

    image_files = await download_images(url)

    if not image_files:
        await message.reply_text("❌ No images found after download.")
        return

    for image_file in image_files:
        image_path = os.path.join("downloads", image_file)
        await client.send_photo(message.chat.id, photo=image_path)
        os.remove(image_path)

    await message.reply_text("✅ All images sent.")