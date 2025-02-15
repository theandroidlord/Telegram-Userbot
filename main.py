import os
import logging
import asyncio
from pyrogram import Client
from aiohttp import web

# Load environment variables
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
SESSION_STRING = os.getenv("PYROGRAM_SESSION_STRING", "")

if not SESSION_STRING:
    raise ValueError("PYROGRAM_SESSION_STRING is missing from environment variables!")

# Initialize Pyrogram client
app = Client("userbot", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

# Import commands from separate files
from commands.hi_command import handle_hi_command  # Make sure the file exists

# Start the bot
async def start_bot():
    await app.start()
    print("Userbot is running!")

# Port binding fix for Render
async def run_server():
    async def handle(request):
        return web.Response(text="Userbot is running!")

    app_runner = web.AppRunner(web.Application())
    await app_runner.setup()
    site = web.TCPSite(app_runner, "0.0.0.0", int(os.getenv("PORT", "10000")))
    await site.start()
    print("Server is running on port", os.getenv("PORT", "10000"))

async def main():
    await asyncio.gather(start_bot(), run_server())

if __name__ == "__main__":
    asyncio.run(main())