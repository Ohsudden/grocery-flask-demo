import aiogram
from aiogram import Bot, Dispatcher, types
import asyncio
import logging
from flask import Flask, jsonify
from flask_cors import CORS
import concurrent.futures

import db

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
# Apply CORS to the entire Flask app
CORS(app, resources={r"/get_balance/*": {"origins": "https://ohsudden.github.io"}})

@app.route('/')
def hello():
    return 'Main page'

@app.route('/get_balance')
def balancepage():
    return 'This is the page for balances'

@app.route('/get_balance/<int:user_id>', methods=['GET'])
def get_balance(user_id):
    # Fetch user balance from the database
    balance = db.get_balance(user_id) / 1e9  # Convert from nanoton to TON
    if balance is None:
        balance = 0
    response = jsonify({'balance': f'{balance:.2f}'})
    response.headers.add("Access-Control-Allow-Origin", "https://ohsudden.github.io")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return response

BOT_TOKEN = '7386401380:AAGO96QtljKyPQ32bj85e4s_VznJAOpXLb8'

loop = asyncio.new_event_loop()
bot = Bot(BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, loop)

async def start_polling():
    from handlers import dp  # Ensure handlers are imported here
    await dp.start_polling()

def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(run_flask)
        loop.run_until_complete(start_polling())
