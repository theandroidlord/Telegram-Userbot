from pyrogram import Client, filters

async def start(client, message):
    await message.reply_text("Userbot is active!")

start_cmd = filters.command("start", prefixes=["/", "!"]) & filters.me