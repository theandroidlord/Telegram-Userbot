import os
import logging
import asyncio
from pyrogram import Client

# Import keep-alive server
from keepalive_render import start_keepalive  

# Load environment variables
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
SESSION_STRING = os.getenv("PYROGRAM_SESSION_STRING", "")

if not SESSION_STRING:
    raise ValueError("PYROGRAM_SESSION_STRING is missing from environment variables!")

# Initialize Pyrogram client
app = Client("userbot", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

# Import & register commands
from commands.weather_command import register_weather_command  

register_weather_command(app)

async def main():
    """Starts both the userbot and the keep-alive server."""
    # Start the keep-alive server
    keepalive_task = asyncio.create_task(start_keepalive())

    # Start the Telegram userbot
    await app.start()
    print("Userbot is running!")

    try:
        await asyncio.Event().wait()  # Keep running indefinitely
    finally:
        await app.stop()
        keepalive_task.cancel()
        try:
            await keepalive_task
        except asyncio.CancelledError:
            pass
        print("Userbot stopped.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())