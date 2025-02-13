import os
import logging
from pyrogram import Client, filters
from flask import Flask

# Enable logging
logging.basicConfig(level=logging.INFO)

# Load API credentials from environment variables
API_ID = int(os.getenv("API_ID", "123456"))  # Replace with your API ID
API_HASH = os.getenv("API_HASH", "your_api_hash")  # Replace with your API Hash
PORT = int(os.getenv("PORT", 8080))  # Render provides a PORT

# Initialize Flask app for port binding
app = Flask(__name__)

@app.route("/")
def home():
    return "Userbot is running."

# Initialize Pyrogram client
bot = Client("userbot", api_id=API_ID, api_hash=API_HASH)

@bot.on_message(filters.command("hi", prefixes=["/", "!"]) & filters.me)
async def greet_user(client, message):
    if len(message.command) < 2:
        await message.reply("Usage: /hi <name>")
        return
    
    name = " ".join(message.command[1:])  # Get name from command
    await message.reply(f"Hello {name}, how are you?")

if __name__ == "__main__":
    # Start Flask server in the background
    from threading import Thread
    Thread(target=lambda: app.run(host="0.0.0.0", port=PORT, debug=False)).start()
    
    # Run the userbot
    bot.run()