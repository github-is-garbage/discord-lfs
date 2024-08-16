from bot import Bot
import discord
from pathlib import Path

from image_helper import ProcessFileContent

from temphelp import canthing

@Bot.tree.command(name = "upload")
async def upload(interaction: discord.Interaction, path: str, channel: discord.TextChannel = None):
	if not canthing(interaction): # TODO: Remove this
		return await interaction.response.send_message("No")

	FilePath = Path(path)

	if not FilePath.is_file():
		return await interaction.response.send_message("File does not exist!")

	File = open(path, "rb")
	Content = File.read()
	File.close()

	if len(Content) < 1:
		return await interaction.response.send_message("File is empty!")

	Channel = channel if channel is not None else interaction.channel

	try:
		await interaction.response.send_message("Starting processing...")

		await ProcessFileContent(interaction, FilePath, Content, Channel)
	except Exception as Error:
		print(Error)

		await interaction.edit_original_response(content = "Failed for some reason (Check bot console)")
