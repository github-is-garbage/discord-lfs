from bot import Bot
import discord
import os

@Bot.event
async def on_ready():
	print("Connected to Discord")

	print("Syncing commands")
	TestServer = discord.Object(int(os.environ.get("GUILD_ID"))) # TODO: Make this better?

	Bot.tree.copy_global_to(guild = TestServer)
	await Bot.tree.sync(guild = TestServer)

	print(f"Ready as {Bot.user}")
