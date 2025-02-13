import os
import shlex
import asyncio
from pyrogram import Client, filters

@app.on_message(filters.command("gld_img") & filters.me)
async def gld_img_cmd(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /gld_img <URL>")
        return

    url = message.command[1]
    await message.reply_text(f"Extracting image links from {url}...")

    # Extract media links
    process = await asyncio.create_subprocess_exec(
        *shlex.split(f'gallery-dl --simulate {url}'),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, _ = await process.communicate()
    media_urls = [line.strip() for line in stdout.decode().splitlines() if line.strip()]

    # Filter for image links
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    image_urls = [url for url in media_urls if any(url.lower().endswith(ext) for ext in image_extensions)]

    if not image_urls:
        await message.reply_text("❌ No images found.")
        return

    await message.reply_text(f"Found {len(image_urls)} images. Downloading...")

    for media_url in image_urls:
        await asyncio.create_subprocess_exec(
            *shlex.split(f'gallery-dl {media_url}')
        )

        # Check if file exists in the downloads folder
        downloaded_files = os.listdir("downloads")
        if not downloaded_files:
            await message.reply_text("❌ No image found after download.")
            continue

        for file in downloaded_files:
            file_path = os.path.join("downloads", file)
            await client.send_document(message.chat.id, file_path)
            os.remove(file_path)  # Delete after sending
            await asyncio.sleep(5)  # Wait before sending the next file

    await message.reply_text("✅ All images sent.")