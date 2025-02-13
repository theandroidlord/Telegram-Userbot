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

# Register command handlers
app.add_handler(filters.command("gld_img") & filters.me, gld_img_cmd)
app.add_handler(filters.command("gld_vid") & filters.me, gld_vid_cmd)

# Start command to check if bot is alive
@app.on_message(filters.command("start") & filters.me)
async def start_cmd(client, message):
    await message.reply_text("✅ Userbot is active!")

# Web server for Render (Port Binding Fix)
async def run_web():
    async def handle(request):
        return web.Response(text="Userbot is running!")

    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 10000)))
    await site.start()

# Run Pyrogram bot and web server separately
async def main():
    # Start Pyrogram bot
    bot_task = asyncio.create_task(app.run())  

    # Start web server for Render
    web_task = asyncio.create_task(run_web())  

    # Keep both running
    await asyncio.gather(bot_task, web_task)

if __name__ == "__main__":
    logging.info("🚀 Starting Userbot with Render port binding fix...")
    asyncio.run(main())