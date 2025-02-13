import logging
import os
import asyncio
import pyrogram
import pandas as pd
import gspread
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram API credentials
API_ID = int(os.getenv("API_ID", "YOUR_API_ID"))
API_HASH = os.getenv("API_HASH", "YOUR_API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING", "YOUR_SESSION_STRING")

# Google Sheets setup
gc = gspread.service_account(filename="google_credentials.json")
sheet = gc.open("Telegram Userbot Storage").sheet1  # Change to your sheet name

# Flask app for Render port binding
app = Flask(__name__)

@app.route("/")
def home():
    return "Userbot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)), threaded=True)

# Start Flask in a separate thread
Thread(target=run_flask).start()

# Initialize Pyrogram Client
app = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# Command: /hi Name
@app.on_message(filters.command("hi") & filters.me)
async def greet(client, message):
    if len(message.command) > 1:
        name = " ".join(message.command[1:])
        await message.reply_text(f"Hello {name}, How are You?")
    else:
        await message.reply_text("Usage: /hi [Name]")

# Command: /store (Text) (Description) (Author) [Reply to a message]
@app.on_message(filters.command("store") & filters.reply & filters.me)
async def store_message(client, message):
    args = message.text.split(" ", 3)
    if len(args) < 4:
        await message.reply_text("Usage: /store (Text) (Description) (Author) [Reply to a message]")
        return

    text, description, author = args[1], args[2], args[3]

    # Get message link
    chat_id = message.chat.id
    msg_id = message.reply_to_message.id
    message_link = f"https://t.me/c/{str(chat_id).replace('-100', '')}/{msg_id}"

    # Store in Google Sheets
    sheet.append_row([message_link, text, description, author])
    await message.reply_text(f"Stored: {text} - {description} (by {author})")

# Command: /restore (Author)
@app.on_message(filters.command("restore") & filters.me)
async def restore_messages(client, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text("Usage: /restore (Author)")
        return

    author = args[1]
    data = sheet.get_all_values()
    
    response = f"Messages stored by {author}:\n"
    found = False

    for row in data:
        if len(row) == 4 and row[3] == author:
            found = True
            response += f"- [{row[1]}]({row[0]}) - {row[2]}\n"

    if found:
        await message.reply_text(response, disable_web_page_preview=True)
    else:
        await message.reply_text(f"No messages found for {author}.")

# Run the Userbot
app.run()