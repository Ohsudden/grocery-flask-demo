import aiogram
from aiogram import Bot, Dispatcher, executor, types
import asyncio
import logging
from flask import Flask, jsonify
from flask_cors import CORS

import db

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

@app.route('/get_balance/<int:user_id>', methods=['GET'])
def get_balance(user_id):
    # Fetch user balance from the database
    balance = db.get_balance(user_id) / 1e9  # Convert from nanoton to TON
    if balance is None:
        balance = 0
    return jsonify({'balance': f'{balance:.2f}'})

BOT_TOKEN = '7386401380:AAGO96QtljKyPQ32bj85e4s_VznJAOpXLb8'

loop = asyncio.new_event_loop();
bot = Bot(BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, loop)


if __name__ == "__main__":
    from handlers import dp
    executor.start_polling(dp)
    app.run(host="0.0.0.0")
