import discord
from discord.ext import commands

Intentions = discord.Intents.default()
Intentions.message_content = True

Bot = commands.Bot(
	command_prefix = ";",
	intents = Intentions,

	case_insensitive = True
)
