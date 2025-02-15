import os
import logging
import asyncio
from pyrogram import Client
from aiohttp import web
from dotenv import load_dotenv
from commands.hi_command import hi_command

# Load environment variables
load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PYROGRAM_STRING_SESSION = os.getenv("PYROGRAM_STRING_SESSION")

# Logging setup
logging.basicConfig(level=logging.INFO)

# Initialize Pyrogram Client
app = Client("userbot", session_string=PYROGRAM_STRING_SESSION, api_id=API_ID, api_hash=API_HASH)

# Import commands
app.add_handler(hi_command)

# Render port binding fix
async def run_server():
    async def handle(request):
        return web.Response(text="Userbot is running!")

    app_runner = web.AppRunner(web.Application())
    app_runner.app.router.add_get("/", handle)
    await app_runner.setup()
    site = web.TCPSite(app_runner, "0.0.0.0", int(os.getenv("PORT", 10000)))
    await site.start()

async def main():
    await asyncio.gather(app.start(), run_server())

if __name__ == "__main__":
    asyncio.run(main())