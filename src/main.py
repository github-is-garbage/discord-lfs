from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

import os
from bot import Bot

import mobile

Bot.run(os.environ.get("BOT_TOKEN"))
