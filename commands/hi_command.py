from pyrogram import Client, filters

@app.on_message(filters.command("Hi") & filters.me)
async def handle_hi_command(client, message):
    name = message.text.split(maxsplit=1)[-1] if len(message.text.split()) > 1 else "there"
    await message.reply_text(f"Hi {name}, how are you?")