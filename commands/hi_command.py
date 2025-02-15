from pyrogram import filters
from pyrogram.types import Message
from pyrogram import Client

@Client.on_message(filters.command("Hi", prefixes="/") & filters.me)
async def hi_command(client, message: Message):
    name = " ".join(message.command[1:]) if len(message.command) > 1 else "there"
    await message.reply_text(f"Hi {name}, how are you?")