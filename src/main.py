import os
from dotenv import load_dotenv, find_dotenv

dotenv_location = find_dotenv()

if len(dotenv_location) > 0:
	load_dotenv(dotenv_location)

	BOT_TOKEN = os.environ.get("BOT_TOKEN")

	print(BOT_TOKEN)
else:
	print("Can't find .env - Aborting")
