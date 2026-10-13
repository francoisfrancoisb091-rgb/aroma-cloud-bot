from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
    return "AROMA CLOUD BOT IS ALIVE!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def start_keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()