from bot import Bot
import discord

from download_helper import DownloadMessageLink

@Bot.tree.command(name = "download")
async def download(interaction: discord.Interaction, message_link: str):
	await interaction.response.send_message("Fetching message...")

	await DownloadMessageLink(interaction ,message_link)
