from bot import Bot
import discord

@Bot.tree.command(name = "upload")
async def upload(interaction: discord.Interaction, path: str):
	if not interaction.user.guild_permissions.administrator: return await interaction.response.send_message("No")
	if not interaction.user.resolved_permissions.administrator: return await interaction.response.send_message("No")

	await interaction.response.send_message(f"Pong! {path}")
