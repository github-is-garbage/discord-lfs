from bot import Bot
import discord
import re
import io
import os
import math
import aiohttp
from PIL import Image
from pathlib import Path

async def GetMessage(MessageLink: str):
	Parts = MessageLink.split("/")

	if len(Parts) < 7:
		return None

	try:
		MessageGuildID = int(Parts[4])
		MessageChannelID = int(Parts[5])
		MessageID = int(Parts[6])

		Guild = Bot.get_guild(MessageGuildID)
		if Guild is None: Guild = await Bot.fetch_guild(MessageGuildID)

		Channel = Guild.get_channel(MessageChannelID)
		if Channel is None: Channel = await Guild.fetch_channel(MessageChannelID)

		Message = await Channel.fetch_message(MessageID)

		return Message
	except Exception as Error:
		print(Error)

		return None

def GetChunkCount(Message: discord.Message):
	Searcher = r"Chunk Count: `(\d+)`"
	Match = re.search(Searcher, Message.content)

	if Match:
		return int(Match.group(1))
	else:
		return 1

def GetFileNamePath(Message: discord.Message):
	Searcher = r"Filename: `([^`]+)`"
	Match = re.search(Searcher, Message.content)

	if Match:
		return Path(Match.group(1))
	else:
		return ".txt"

async def GetMessageReferences(Message: discord.Message):
	TotalChunkCount = GetChunkCount(Message)
	TargetID = str(Message.id)

	Messages = [ Message ]

	if TotalChunkCount != len(Messages):
		# Find the references
		async for FoundMessage in Message.channel.history(after = Message, limit = TotalChunkCount): # The "limit" parameter may be incorrect if multiple uploads happened at the same time. Unfortunately bots don't have access to search endpoint :[
			if TargetID in FoundMessage.content:
				Messages.append(FoundMessage)

				if len(Messages) >= TotalChunkCount:
					break

	# TODO: Sort Messages to ensure chunk order

	return Messages

async def URLToBuffer(URL: str):
	DownloadClient = aiohttp.ClientSession()

	Response = await DownloadClient.get(URL)
	Response.raise_for_status()

	Buffer = io.BytesIO(await Response.read())
	Buffer.seek(0)

	Response.close()
	await DownloadClient.close()

	return Buffer

async def DownloadMessageImage(Message: discord.Message):
	Attachment = Message.attachments[0]
	if Attachment is None: return None

	Buffer = await URLToBuffer(Attachment.url)

	EncodedImage = Image.open(Buffer).convert("RGB")
	Pixels = EncodedImage.load()
	Width, Height = EncodedImage.size

	Binary = ""

	for y in range(Height):
		for x in range(Width):
			Pixel = Pixels[x, y]

			# TODO: See if pre-defining these tuples speeds things up
			if Pixel == (255, 0, 0):
				break

			if Pixel == (0, 0, 0):
				Binary += "1"
			else:
				Binary += "0"

			# TODO: Check transparency

	EncodedImage.close()
	Buffer.close()

	return Binary

def FindDownloadsFolder():
	if os.name == "nt":
		return Path(os.getenv("USERPROFILE")) / "Downloads"
	else:
		# Hope you're on posix!
		return Path.home() / "Downloads"

def BinaryToBytes(Binary: str):
	Padding = len(Binary) % 8

	if Padding != 0:
		Binary = Binary.zfill(len(Binary) + (8 - Padding))

	ByteCount = math.floor(len(Binary) / 8)
	Converted = int(Binary, 2)

	return Converted.to_bytes(ByteCount, "big")

async def CompileMessages(Interaction: discord.Interaction, Messages: list):
	FinalBinary = ""
	FileNamePath = GetFileNamePath(Messages[0])

	MessageCount = len(Messages)

	for i, Message in enumerate(Messages):
		await Interaction.edit_original_response(content = f"Downloading message `{i + 1}` / `{MessageCount}`")

		Binary = await DownloadMessageImage(Message)

		FinalBinary += Binary

	FinalBytes = BinaryToBytes(FinalBinary)

	return FinalBytes, FileNamePath

async def DownloadMessageLink(Interaction: discord.Interaction, MessageLink: str):
	SourceMessage = await GetMessage(MessageLink)

	if SourceMessage is None:
		return await Interaction.edit_original_response(content = "Invalid message link")

	References = await GetMessageReferences(SourceMessage)
	FinalBytes, FileNamePath = await CompileMessages(Interaction, References)

	FinalFolderPath = FindDownloadsFolder() / "DiscordLFS"
	FinalFolderPath.mkdir(parents = True, exist_ok = True) # Create if not exists

	FinalFilePath = (FinalFolderPath / FileNamePath).resolve()

	File = open(FinalFilePath, "wb")
	File.write(FinalBytes)
	File.close()

	await Interaction.edit_original_response(content = f"Downloaded `{FileNamePath}` to `{FinalFilePath}`")
