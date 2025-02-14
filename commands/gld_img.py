import asyncio
import shlex
import os
from pyrogram import Client

async def gld_img_cmd(client: Client, message):
    if len(message.command) < 2:
        await message.reply_text("❌ Please provide a URL.")
        return

    url = message.command[1]
    await message.reply_text(f"🔄 Fetching images from {url}...")

    # Get media download links
    process = await asyncio.create_subprocess_exec(
        *shlex.split(f'gallery-dl --get-urls {url}'),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, _ = await process.communicate()
    media_urls = stdout.decode().splitlines()

    # Filter only image files
    image_urls = [link for link in media_urls if link.lower().endswith((".jpg", ".png", ".jpeg", ".gif", ".webp"))]

    if not image_urls:
        await message.reply_text("❌ No images found.")
        return

    await message.reply_text(f"✅ Found {len(image_urls)} images. Downloading...")

    # Process each image one by one
    for img_url in image_urls:
        img_process = await asyncio.create_subprocess_exec(
            *shlex.split(f'gallery-dl {img_url}'),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await img_process.communicate()

        # Find downloaded files
        downloaded_files = [f for f in os.listdir() if f.endswith((".jpg", ".png", ".jpeg", ".gif", ".webp"))]
        if not downloaded_files:
            await message.reply_text("❌ No image found after download.")
            continue

        # Send each image and delete it
        for img_file in downloaded_files:
            try:
                await message.reply_document(img_file)  # Send as document
            except Exception as e:
                await message.reply_text(f"⚠️ Failed to send {img_file}: {e}")
            os.remove(img_file)
            await asyncio.sleep(5)  # 5-second delay

    await message.reply_text("✅ All images sent.")

# ✅ Ensure function is correctly imported
__all__ = ["gld_img_cmd"]