import os
import aiohttp
from pyrogram import Client, filters

@app.on_message(filters.command("weather") & filters.me)
async def handle_weather_command(client, message):
    # Extract city name
    command_parts = message.text.split(" ", 1)
    if len(command_parts) < 2:
        await message.reply_text("Usage: /weather {city}")
        return

    city = command_parts[1]

    # Fetch weather from wttr.in
    url = f"https://wttr.in/{city}?format=%C+%t\nMax:%M Min:%m\nHumidity:%h\nAir Pressure:%P\nWind:%w"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                weather_data = await response.text()
                await message.delete()  # Delete the command message
                await message.reply_text(f"**Weather in {city}, IN:**\n```{weather_data}```")
            else:
                await message.reply_text("❌ Failed to fetch weather data.")