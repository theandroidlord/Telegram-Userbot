import os
import asyncio
import threading
from flask import Flask
from pyrogram import Client, filters
from chatgpt import chat_with_gpt

# Load session string from environment variable
SESSION_STRING = os.getenv("PYROGRAM_SESSION_STRING")

# Initialize Pyrogram Client
app = Client("userbot", session_string=SESSION_STRING)

# Flask for port binding (Render requirement)
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Userbot is running!"

def run_flask():
    port = int(os.getenv("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

# Command: /gpt [message]
@app.on_message(filters.command("gpt", prefixes=["/", "!"]) & filters.me)
async def ask_gpt(client, message):
    if len(message.command) > 1:
        query = " ".join(message.command[1:])
        response = chat_with_gpt(query)
        await message.reply_text(response)
    else:
        await message.reply_text("Usage: /gpt [your question]")

# Run Flask in a separate thread
threading.Thread(target=run_flask, daemon=True).start()

# Start the userbot
print("Userbot is running...")
app.run()