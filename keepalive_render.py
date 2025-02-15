from quart import Quart

app = Quart(__name__)

@app.route("/")
async def home():
    return "Userbot is running!"

async def run():
    await app.run_task(host="0.0.0.0", port=10000)

async def keep_alive():
    import asyncio
    asyncio.create_task(run())