from pyrogram import Client, filters

@Client.on_message(filters.command("Hi") & filters.me)
async def handle_hi_command(client, message):
    name = message.text.split(" ", 1)[-1] if " " in message.text else "there"
    await message.reply_text(f"Hi {name}, how are you?")