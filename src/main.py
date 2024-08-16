from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

import os
from bot import bot

import mobile

bot.run(os.environ.get("BOT_TOKEN"))
