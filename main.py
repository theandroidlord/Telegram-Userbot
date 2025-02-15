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

# Import & register commands
from commands.hi_command import register_hi_command  
from commands.weather_command import register_weather_command  

register_hi_command(app)
register_weather_command(app)


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
    server_task = asyncio.create_task(run_server())

    try:
        await asyncio.Event().wait()  # Keep running indefinitely
    finally:
        await app.stop()
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass
        print("Userbot stopped.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())