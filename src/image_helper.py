import discord
import math
import io
from pathlib import Path
from PIL import Image

PIXELS_PER_ROW = 2048
CHUNK_SIZE = 16 * 1024 * 1024

def StringToBinary(String: str):
	return "".join(format(i, "08b") for i in String)

def BinaryToImage(Binary: str):
	Length = len(Binary)

	Rows = math.ceil(Length / PIXELS_PER_ROW)

	Constructed = Image.new("RGB", (PIXELS_PER_ROW, Rows), "#FFFFFF")

	for Row in range(0, Rows):
		for Pixel in range(0, PIXELS_PER_ROW):
			Index = ((Row - 1) * PIXELS_PER_ROW) + Pixel

			if Index >= Length:
				break # Hit the end

			Character = Binary[Index]

			Constructed.putpixel((Pixel, Row), (0, 0, 0) if Character == "1" else (255, 255, 255))

	return Constructed

def SplitBinaryData(Binary: str):
	return [Binary[i:i + CHUNK_SIZE] for i in range(0, len(Binary), CHUNK_SIZE)]

async def ProcessFileContent(Interaction: discord.Interaction, FilePath: Path, Content: str, Channel: discord.TextChannel):
	Binary = StringToBinary(Content)

	if len(Binary) < 1:
		return await Interaction.edit_original_response(content = "Failed to convert to binary data")

	BinaryChunks = SplitBinaryData(Binary)
	ChunkCount = len(BinaryChunks)
	TotalSize = 0

	# Turn binary string into a pretty picture
	await Interaction.edit_original_response(content = f"Constructing...\n(May take a while)\n\nChunk Count: `{ChunkCount}`")

	InitialMessage = None

	for i, Chunk in enumerate(BinaryChunks):
		# print(f"Constructing image for chunk #{i}")
		ConstructedImage = BinaryToImage(Chunk)

		# Plop it into a memory buffer
		# print(f"Saving chunk #{i} to buffer")
		Buffer = io.BytesIO()
		ConstructedImage.save(Buffer, "PNG")

		TotalSize += Buffer.getbuffer().nbytes
		Buffer.seek(0)

		# Upload to Discord
		File = discord.File(Buffer, "constructed.png")

		# print(f"Uploading chunk #{i}")

		if InitialMessage is None:
			InitialMessage = await Channel.send(f"Filename: `{FilePath.name}`\nPath: `{FilePath.resolve()}`\nChunk Count: `{ChunkCount}`", file = File)
		else:
			# The "Reference" and "Chunk Number" will be used in the download step
			await Channel.send(f"Filename: `{FilePath.name}`\nPath: `{FilePath.resolve()}`\nReference: `{InitialMessage.id}`\nChunk Number: `{i}`", file = File)

		Buffer.close()
		ConstructedImage.close()

	# Respond with link to upload message
	MessageGuildID = InitialMessage.guild.id
	MessageChannelID = Channel.id
	MessageID = InitialMessage.id

	MessageLink = f"https://discord.com/channels/{MessageGuildID}/{MessageChannelID}/{MessageID}"

	await Interaction.edit_original_response(content = f"Uploaded [here]({MessageLink})\nTotal size: {TotalSize} bytes")
