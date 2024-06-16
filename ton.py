import requests
import asyncio

# Aiogram
from aiogram import Bot
from aiogram.types import ParseMode

# We also need config and database here

import db
import config

async def start():
    try:
        # Try to load last_lt from file
        with open('last_lt.txt', 'r') as f:
            last_lt = int(f.read())
    except FileNotFoundError:
        # If file not found, set last_lt to 0
        last_lt = 0

    # We need the Bot instance here to send deposit notifications to users
    bot = Bot(token=config.BOT_TOKEN)

    while True:

        await asyncio.sleep(2)

        # API call to TON Center that returns last 100 transactions of our wallet
        resp = requests.get(f'{config.API_BASE_URL}/api/v2/getTransactions?'
                            f'address={config.DEPOSIT_ADDRESS}&limit=100&'
                            f'archival=true&api_key={config.API_KEY}').json()

        # If call was not successful, try again
        if not resp['ok']:
            continue

        for tx in resp['result']:
            # LT is Logical Time and Hash is hash of our transaction
            lt, hash = int(tx['transaction_id']['lt']), tx['transaction_id']['hash']

            # If this transaction's logical time is lower than our last_lt,
            # we already processed it, so skip it

            if lt <= last_lt:
                continue
            value = int(tx['in_msg']['value'])

            if value > 0:
                uid = tx['in_msg']['message']

                if not uid.isdigit():
                    continue

                uid = int(uid)

                if not db.check_user(uid):
                    continue

                db.add_balance(uid, value)

                await bot.send_message(uid, 'Deposit confirmed!\n'
                                            f'*+{value / 1e9:.2f} TON*',
                                       parse_mode=ParseMode.MARKDOWN)
            last_lt = lt
            with open('last_lt.txt', 'w') as f:
                f.write(str(last_lt))