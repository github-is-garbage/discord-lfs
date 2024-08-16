from bot import Bot
import discord

@Bot.event
async def on_ready():
	print("Connected to Discord")

	print("Syncing commands")
	TestServer = discord.Object(642793766188744715) # TODO: Make it not this

	Bot.tree.copy_global_to(guild = TestServer)
	await Bot.tree.sync(guild = TestServer)

	print(f"Ready as {Bot.user}")
