from flask import Flask
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "Userbot is running!"

def run():
    app.run(host="0.0.0.0", port=10000, threaded=True)

def keep_alive():
    server = threading.Thread(target=run, daemon=True)
    server.start()