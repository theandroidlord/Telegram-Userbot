import os
import asyncio
from pyrogram import Client, filters

# Load session string from environment variable
SESSION_STRING = os.getenv("PYROGRAM_SESSION_STRING")

# Create Pyrogram client (running on your main account)
app = Client("my_account", session_string=SESSION_STRING)

# Command: /hi Name
@app.on_message(filters.command("hi", prefixes=["/", "!"]) & filters.me)
async def greet(client, message):
    if len(message.command) > 1:
        name = " ".join(message.command[1:])
        await message.reply_text(f"Hello {name}, how are you?")
    else:
        await message.reply_text("Hello! How are you?")

# Start the bot
print("Running Pyrogram bot...")
app.run()