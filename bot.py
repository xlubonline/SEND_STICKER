import telebot
import os
import random
import threading
import time
from flask import Flask
from dotenv import load_dotenv

load_dotenv("config.env")
# === Configuration ===
TOKEN = os.environ.get("BOT_TOKEN")
GROUP_CHAT_ID = os.environ.get("GROUP_CHAT_ID")
STICKER_FOLDER = 'stickerdb'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
last_sticker_message_id = None

# === Flask route to keep alive ===
@app.route('/')
def home():
    return "Bot is alive!", 200

# === Background sticker sending ===
def send_and_replace_sticker():
    global last_sticker_message_id

    while True:
        try:
            # Delete old sticker
            if last_sticker_message_id:
                try:
                    bot.delete_message(GROUP_CHAT_ID, last_sticker_message_id)
                    print(f"Deleted old sticker: {last_sticker_message_id}")
                except Exception as e:
                    print(f"Delete failed: {e}")

            # Pick a random sticker
            stickers = [f for f in os.listdir(STICKER_FOLDER) if f.endswith('.webp')]
            if not stickers:
                print("No stickers in folder.")
                time.sleep(120)
                continue

            sticker_path = os.path.join(STICKER_FOLDER, random.choice(stickers))

            with open(sticker_path, 'rb') as f:
                sent = bot.send_sticker(GROUP_CHAT_ID, f)
                last_sticker_message_id = sent.message_id
                print(f"Sent: {sticker_path}")

        except Exception as e:
            print(f"Error sending sticker: {e}")

        time.sleep(120)

# === Start everything ===
if __name__ == '__main__':
    # Start background sticker task
    threading.Thread(target=send_and_replace_sticker, daemon=True).start()

    # Start bot polling in its own thread
    threading.Thread(target=bot.infinity_polling, daemon=True).start()

    # Run Flask app on 0.0.0.0 to expose it for pings
    app.run(host='0.0.0.0', port=8080)
