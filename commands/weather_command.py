import aiohttp
import os
from pyrogram import Client, filters

# AccuWeather API Key (Set this as an environment variable in Render)
API_KEY = os.getenv("ACCUWEATHER_API_KEY")

async def get_location_key(city):
    """Fetch location key for the given city from AccuWeather API."""
    url = f"https://dataservice.accuweather.com/locations/v1/cities/search?apikey={API_KEY}&q={city}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data:
                    return data[0]["Key"]  # Return the first city's location key
            return None

async def get_weather_data(location_key):
    """Fetch weather data using the location key."""
    url = f"https://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={API_KEY}&details=true"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data[0] if data else None
            return None

def register_weather_command(app: Client):
    @app.on_message(filters.command("weather") & filters.me)
    async def handle_weather_command(client, message):
        command_parts = message.text.split(" ", 1)
        if len(command_parts) < 2:
            await message.reply_text("Usage: `/weather {city}`")
            return

        city = command_parts[1]
        await message.delete()  # Delete the command message

        location_key = await get_location_key(city)
        if not location_key:
            await message.reply_text(f"❌ City '{city}' not found.")
            return

        weather_data = await get_weather_data(location_key)
        if not weather_data:
            await message.reply_text(f"❌ Failed to fetch weather for {city}.")
            return

        # Extract data
        temp = weather_data["Temperature"]["Metric"]["Value"]
        max_temp = weather_data.get("RealFeelTemperature", {}).get("Metric", {}).get("Value", "N/A")
        min_temp = weather_data.get("RealFeelTemperatureShade", {}).get("Metric", {}).get("Value", "N/A")
        humidity = weather_data["RelativeHumidity"]
        pressure = weather_data["Pressure"]["Metric"]["Value"]
        wind_speed = weather_data["Wind"]["Speed"]["Metric"]["Value"]
        wind_direction = weather_data["Wind"]["Direction"]["Localized"]
        weather_text = weather_data["WeatherText"]

        # Format response
        response = f"🌤 **Weather in {city}, IN:**\n" \
                   f"🌡 {temp}°C, {weather_text}\n\n" \
                   f"🔺 Max: {max_temp}°C  |  🔻 Min: {min_temp}°C\n" \
                   f"💧 Humidity: {humidity}%\n" \
                   f"🌬 Wind: {wind_speed}m/s {wind_direction}\n" \
                   f"🛑 Pressure: {pressure} hPa"

        await message.reply_text(response)