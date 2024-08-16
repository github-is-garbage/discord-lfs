from bot import Bot
import discord

from download_helper import DownloadMessageLink

from temphelp import canthing

@Bot.tree.command(name = "download")
async def download(interaction: discord.Interaction, message_link: str):
	if not canthing(interaction): # TODO: Remove this
		return await interaction.response.send_message("No")

	await interaction.response.send_message("Fetching message...")

	await DownloadMessageLink(interaction ,message_link)
