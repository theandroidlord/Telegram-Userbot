import os
import logging
import asyncio
from pyrogram import Client

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

async def log_status():
    while True:
        print("Pyrogram: OK")
        await asyncio.sleep(2)  # Logs every 2 seconds to confirm bot is active

async def main():
    await app.start()
    print("Userbot is running!")

    # Start logging status
    log_task = asyncio.create_task(log_status())

    try:
        await asyncio.Event().wait()  # Keep running indefinitely
    finally:
        await app.stop()
        log_task.cancel()
        try:
            await log_task
        except asyncio.CancelledError:
            pass
        print("Userbot stopped.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Render port binding fix
    port = int(os.getenv("PORT", "10000"))
    asyncio.run(main())