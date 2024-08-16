from bot import Bot
import discord
from temphelp import canthing

@Bot.tree.command(name = "upload")
async def upload(interaction: discord.Interaction, path: str):
	if not canthing(interaction): # TODO: Remove this
		return await interaction.response.send_message("No")

	await interaction.response.send_message(f"Pong! {path}")
