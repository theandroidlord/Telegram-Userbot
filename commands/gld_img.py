import asyncio
import os
from pyrogram import Client, filters
import subprocess

async def download_images(url):
    try:
        process = await asyncio.create_subprocess_exec(
            "gallery-dl", "--skip-metadata", "-f", "jpg,png", url,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        await process.communicate()
        return process.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False

@Client.on_message(filters.command("gld_img", prefixes=["/", "!"]) & filters.me)
async def gld_img_cmd(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: `/gld_img <URL>`")
        return

    url = message.command[1]
    await message.reply_text("📥 Downloading images...")

    success = await download_images(url)
    if success:
        await message.reply_text("✅ Images downloaded successfully!")
    else:
        await message.reply_text("❌ Failed to download images.")