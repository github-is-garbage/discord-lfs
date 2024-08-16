from bot import Bot

@Bot.event
async def on_ready():
	print(f"Connected to Discord as {Bot.user}")
