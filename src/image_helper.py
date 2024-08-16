import discord
import math
import io
from pathlib import Path
from PIL import Image

PIXELS_PER_ROW = 1000

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

async def ProcessFileContent(Interaction: discord.Interaction, FilePath: Path, Content: str, Channel: discord.TextChannel):
	Binary = StringToBinary(Content)

	if len(Binary) < 1:
		return await Interaction.edit_original_response(content = "Failed to convert to binary data")

	# Turn binary string into a pretty picture
	await Interaction.edit_original_response(content = "Constructing image...\n(May take a while)")
	ConstructedImage = BinaryToImage(Binary)

	# Plop it into a memory buffer
	await Interaction.edit_original_response(content = "Saving image to buffer...")

	Buffer = io.BytesIO()
	ConstructedImage.save(Buffer, "PNG")

	BufferSize = Buffer.getbuffer().nbytes
	Buffer.seek(0)

	# Upload to Discord
	File = discord.File(Buffer, "constructed.png")

	await Interaction.edit_original_response(content = f"Uploading image...\nTotal size: {BufferSize} bytes")
	ChannelMessage = await Channel.send(f"Filename: `{FilePath.name}`\nPath: `{FilePath.resolve()}`", file = File)

	# Respond with link to upload message
	MessageGuildID = ChannelMessage.guild.id
	MessageChannelID = Channel.id
	MessageID = ChannelMessage.id

	MessageLink = f"https://discord.com/channels/{MessageGuildID}/{MessageChannelID}/{MessageID}"

	await Interaction.edit_original_response(content = f"Uploaded [here]({MessageLink})\nTotal size: {BufferSize} bytes")

	Buffer.close()
	ConstructedImage.close()
