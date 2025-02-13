import os
import logging
import asyncio
import firebase_admin
from firebase_admin import credentials, firestore
from pyrogram import Client, filters

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Load Firebase credentials
cred = credentials.Certificate("firebase.json")
if not firebase_admin._apps:  # Ensure Firebase is initialized only once
    firebase_admin.initialize_app(cred)

# Firestore database instance
db = firestore.client()

# Environment variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

# Create a Pyrogram Client (Userbot)
app = Client("my_account", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)


@app.on_message(filters.command("hi"))
async def hi_command(client, message):
    name = " ".join(message.command[1:]) or "there"
    await message.reply_text(f"Hello {name}, How are you?")


@app.on_message(filters.command("store") & filters.reply)
async def store_command(client, message):
    args = message.text.split(maxsplit=3)
    if len(args) < 4:
        await message.reply_text("Usage: /store <Title> <Description> <Author> (Reply to a message)")
        return
    
    title, description, author = args[1], args[2], args[3]
    message_link = f"https://t.me/c/{message.chat.id}/{message.reply_to_message.message_id}"

    doc_ref = db.collection("stored_messages").document()
    data = {
        "text": title,
        "description": description,
        "author": author,
        "message_link": message_link
    }
    await asyncio.to_thread(doc_ref.set, data)  # Prevents blocking the event loop

    await message.reply_text(f"Stored successfully: {title} - {description}")


@app.on_message(filters.command("restore"))
async def restore_command(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply_text("Usage: /restore <Author>")
        return
    
    author = args[1]
    query = db.collection("stored_messages").where("author", "==", author).stream()
    results = await asyncio.to_thread(list, query)  # Fetch documents in a separate thread

    if not results:
        await message.reply_text(f"No stored messages found for {author}.")
        return

    response = "\n".join(
        [f"{doc.to_dict()['text']}: {doc.to_dict()['message_link']}" for doc in results]
    )

    await message.reply_text(response)


# Port binding fix for Render
PORT = int(os.environ.get("PORT", 8080))

async def start():
    logging.info("Starting Telegram userbot...")
    await app.start()
    await asyncio.sleep(1e6)  # Keep it running

if __name__ == "__main__":
    asyncio.run(start())
