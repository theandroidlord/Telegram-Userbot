import os
import logging
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pyrogram import Client
from threading import Thread

# Load environment variables
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
SESSION_STRING = os.getenv("PYROGRAM_SESSION_STRING", "")

if not SESSION_STRING:
    raise ValueError("PYROGRAM_SESSION_STRING is missing from environment variables!")

# Initialize Pyrogram client
app = Client("userbot", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

# Import & register commands
from commands.weather_command import register_weather_command  
register_weather_command(app)

# Simple HTTP server for keep-alive
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Alive")

def run_http_server():
    port = int(os.environ.get("PORT", 10000))  # Use Render's port
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# Run HTTP server in a separate thread
http_thread = Thread(target=run_http_server, daemon=True)
http_thread.start()

async def start_services():
    """Start Pyrogram bot."""
    await app.start()
    print("Userbot is running!")
    await asyncio.Event().wait()  # Keep bot running

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Run bot
    asyncio.run(start_services())