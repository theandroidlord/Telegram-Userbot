import os
import logging
import asyncio
from pyrogram import Client, filters
from aiohttp import web

# Import command handlers
from commands.gld_img import gld_img_cmd
from commands.gld_vid import gld_vid_cmd

# Load session string from environment
SESSION_STRING = os.getenv("STRING_SESSION")

# Ensure session string exists
if not SESSION_STRING:
    raise ValueError("STRING_SESSION environment variable is missing.")

# Initialize Pyrogram Client
app = Client("userbot", session_string=SESSION_STRING)

# Start command to check if bot is alive
@app.on_message(filters.command("start") & filters.me)
async def start_cmd(client, message):
    await message.reply_text("✅ Userbot is active!")

# Register commands correctly
@app.on_message(filters.command("gld_img") & filters.me)
async def call_gld_img(client, message):
    await gld_img_cmd(client, message)

@app.on_message(filters.command("gld_vid") & filters.me)
async def call_gld_vid(client, message):
    await gld_vid_cmd(client, message)

# Run Pyrogram bot
if __name__ == "__main__":
    logging.info("🚀 Starting Userbot...")
    app.run()