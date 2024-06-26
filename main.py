import aiogram
from aiogram import Bot, Dispatcher, types
import asyncio
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
import concurrent.futures

import db

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
# Apply CORS to the entire Flask app
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def hello():
    return 'Main page'

@app.route('/get_balance')
def balancepage():
    return 'This is the page for balances'

@app.route('/get_quest_status')
def qstatus():
    return 'This is a get quest status page'
    
@app.route('/update_quest_status', methods=['GET', 'POST'])
def uqstatus():
    return 'This is an update quest status page'

@app.route('/login')
def ulogin():
    return 'This is a login page'


@app.route('/login/<int:user_id>', methods=['GET'])
def login(user_id):
    if not db.check_user(user_id):
        db.add_new_user(user_id)
    response = jsonify({'success': True})
    response.headers.add("Access-Control-Allow-Origin", "https://ohsudden.github.io")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return response


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


@app.route('/get_quest_status/<int:user_id>', methods=['GET'])
def get_quest_status(user_id):
    status_list = db.get_user_quest_status(user_id)
    return jsonify({'status': status_list})

@app.route('/update_quest_status/<int:user_id>', methods=['GET', 'POST'])
def update_quest_status(user_id):
    if request.method == 'POST':
        data = request.json
        idofTask = data.get('idofTask')  # Get idofTask from the request data
        quest_status = True
        db.update_user_quest_status(user_id, idofTask, quest_status)
        return jsonify({'success': True})
    else:
        return None


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
