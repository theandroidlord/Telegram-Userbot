import os
import logging
import asyncio
from pyrogram import Client, filters
from aiohttp import web

# Load environment variables
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
SESSION_STRING = os.getenv("PYROGRAM_SESSION_STRING", "")

if not SESSION_STRING:
    raise ValueError("PYROGRAM_SESSION_STRING is missing from environment variables!")

# Initialize Pyrogram client
app = Client("userbot", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

# Import commands
import commands.hi_command  # Ensure the file exists

# Web server for Render port binding fix
async def handle(request):
    return web.Response(text="Userbot is running!")

async def run_server():
    app_runner = web.AppRunner(web.Application())
    await app_runner.setup()
    site = web.TCPSite(app_runner, "0.0.0.0", int(os.getenv("PORT", "10000")))
    await site.start()
    print("Server running on port", os.getenv("PORT", "10000"))

async def main():
    await app.start()
    print("Userbot is running!")

    # Start web server concurrently
    await asyncio.gather(run_server())

    await app.idle()  # Keep the bot running

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Userbot stopped.")