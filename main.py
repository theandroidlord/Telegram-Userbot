import os
import logging
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pyrogram import Client, filters
from threading import Thread

# Load environment variables
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
SESSION_STRING = os.getenv("PYROGRAM_SESSION_STRING", "")

if not SESSION_STRING:
    raise ValueError("PYROGRAM_SESSION_STRING is missing from environment variables!")

# Initialize Pyrogram client
app = Client("userbot", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

# Simple HTTP server for keep-alive
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Alive")

def run_http_server():
    port = int(os.environ.get("PORT", 10000))  # Render's port
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f"HTTP server running on port {port}")
    server.serve_forever()

# Run HTTP server in a separate thread
http_thread = Thread(target=run_http_server, daemon=True)
http_thread.start()

@app.on_message(filters.command("ping"))
async def ping(client, message):
    await message.reply("Pong! ✅")

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Userbot is online!")

async def start_services():
    """Start Pyrogram bot."""
    print("Starting Userbot...")
    await app.start()
    print("Userbot is running!")
    await asyncio.Event().wait()  # Keep bot running

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        print("Shutting down bot...")
    finally:
        loop.run_until_complete(app.stop())
        loop.close()