import os
import asyncio
import logging
import firebase_admin
from firebase_admin import credentials, firestore
from pyrogram import Client, filters
from flask import Flask
import threading

# Enable logging
logging.basicConfig(level=logging.INFO)

# Load session string from environment variables
SESSION_STRING = os.getenv("TG_SESSION")
if not SESSION_STRING:
    raise ValueError("TG_SESSION environment variable is not set")

# Firebase setup
FIREBASE_CRED_PATH = "firebase.json"  # Ensure this file is in your root directory
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CRED_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Pyrogram Client
app = Client("userbot", session_string=SESSION_STRING)

# Flask app for Render port binding
server = Flask(__name__)

@server.route('/')
def home():
    return "Userbot is running!"

def run_flask():
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# Start Flask in a separate thread
threading.Thread(target=run_flask, daemon=True).start()

# Command: /hi (name)
@app.on_message(filters.me & filters.command("hi", prefixes="/"))
async def hi_command(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) > 1:
        name = args[1]
        await message.reply_text(f"Hello {name}, How are you?")
    else:
        await message.reply_text("Hello! How are you?")

# Command: /store (text) (description) (author) (when replying to a message)
@app.on_message(filters.me & filters.command("store", prefixes="/") & filters.reply)
async def store_message(client, message):
    args = message.text.split(maxsplit=3)
    if len(args) < 4:
        await message.reply_text("Usage: /store (Text) (Description) (Author) (Reply to a message)")
        return

    title, description, author = args[1], args[2], args[3]
    replied_msg = message.reply_to_message
    if not replied_msg or not replied_msg.link:
        await message.reply_text("Failed to get message link.")
        return

    data = {
        "title": title,
        "description": description,
        "author": author,
        "link": replied_msg.link
    }
    
    db.collection("stored_messages").add(data)
    await message.reply_text(f"Stored message link with title: {title}")

# Command: /restore (author)
@app.on_message(filters.me & filters.command("restore", prefixes="/"))
async def restore_messages(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply_text("Usage: /restore (Author)")
        return

    author = args[1]
    docs = db.collection("stored_messages").where("author", "==", author).stream()
    results = [f"📌 [{doc.to_dict()['title']}]({doc.to_dict()['link']}) - {doc.to_dict()['description']}" for doc in docs]

    if results:
        await message.reply_text("\n".join(results), disable_web_page_preview=True)
    else:
        await message.reply_text(f"No stored messages found for {author}.")

# Start bot
print("Userbot is running...")
app.run()