import os
import logging
import asyncio
from pyrogram import Client
import keepalive_render  # Import Quart web server

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
    await app.start()
    print("Userbot is running!")

    # Start Quart web server in the background to keep bot alive
    asyncio.create_task(keepalive_render.keep_alive())

    try:
        await asyncio.Event().wait()  # Keep running indefinitely
    except asyncio.CancelledError:
        print("Userbot stopped.")

    await app.stop()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())