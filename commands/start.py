from pyrogram import Client, filters

@Client.on_message(filters.command("start") & filters.me)
async def start(client, message):
    await message.reply_text("Userbot is active!")