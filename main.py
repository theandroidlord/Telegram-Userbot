import os
import asyncio
import logging
import firebase_admin
from firebase_admin import credentials, firestore
from pyrogram import Client, filters
from pyrogram.types import Message

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load Firebase credentials
FIREBASE_CREDENTIALS = "firebase_credentials.json"
if not os.path.exists(FIREBASE_CREDENTIALS):
    raise FileNotFoundError("Firebase credentials file is missing!")

cred = credentials.Certificate(FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Port Binding Fix for Render
PORT = int(os.environ.get("PORT", 8080))
async def keep_alive():
    from aiohttp import web
    async def handle(_):
        return web.Response(text="Userbot is running")
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

# Pyrogram Client
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
session_string = os.getenv("SESSION_STRING")  # Store session string for login

app = Client("userbot", api_id=api_id, api_hash=api_hash, session_string=session_string)

# /hi command
@app.on_message(filters.command("hi", prefixes="/"))
async def hi_command(client: Client, message: Message):
    if len(message.command) > 1:
        name = " ".join(message.command[1:])
        await message.reply(f"Hello {name}, How are you?")
    else:
        await message.reply("Hello! How are you?")

# /store command
@app.on_message(filters.command("store", prefixes="/") & filters.reply)
async def store_message(client: Client, message: Message):
    if len(message.command) < 4:
        await message.reply("Usage: /store <Title> <Description> <Author> (Reply to a message)")
        return

    title = message.command[1]
    description = message.command[2]
    author = message.command[3]
    
    if not message.reply_to_message:
        await message.reply("Please reply to a message to store it.")
        return

    message_link = f"https://t.me/c/{message.chat.id}/{message.reply_to_message.message_id}"

    # Save to Firestore
    db.collection("stored_messages").add({
        "title": title,
        "description": description,
        "author": author,
        "message_link": message_link
    })
    
    await message.reply(f"Message stored successfully!\nTitle: {title}\nDescription: {description}\nAuthor: {author}")

# /restore command
@app.on_message(filters.command("restore", prefixes="/"))
async def restore_messages(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("Usage: /restore <Author>")
        return

    author = message.command[1]
    messages_ref = db.collection("stored_messages").where("author", "==", author).stream()

    results = [f"{doc.to_dict()['title']} - {doc.to_dict()['description']}\n{doc.to_dict()['message_link']}" for doc in messages_ref]

    if results:
        await message.reply("\n\n".join(results))
    else:
        await message.reply("No messages found for this author.")

# Run the bot
async def main():
    await keep_alive()
    await app.run()

if __name__ == "__main__":
    asyncio.run(main())