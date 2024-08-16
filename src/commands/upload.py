from bot import Bot
import discord
from pathlib import Path

from image_helper import ProcessFileContent

from temphelp import canthing

@Bot.tree.command(name = "upload")
async def upload(interaction: discord.Interaction, path: str):
	if not canthing(interaction): # TODO: Remove this
		return await interaction.response.send_message("No")

	FilePath = Path(path)

	if not FilePath.is_file():
		return await interaction.response.send_message("File does not exist!")

	File = open(path, "r")
	Content = File.read()
	File.close()

	if len(Content) < 1:
		return await interaction.response.send_message("File is empty!")

	try:
		await ProcessFileContent(interaction, FilePath, Content)
	except Exception as Error:
		print(Error)

		await interaction.response.send_message("Failed for some reason (Check bot console)")
