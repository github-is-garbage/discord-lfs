import discord
import math
import io
from pathlib import Path
from PIL import Image

PIXELS_PER_ROW = 1000

def StringToBinary(String: str):
	return "".join(format(ord(i), "08b") for i in String)

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

async def ProcessFileContent(Interaction: discord.Interaction, FilePath: Path, Content: str):
	Binary = StringToBinary(Content)

	if len(Binary) < 1:
		return await Interaction.response.send_message("Failed to convert to binary data")

	ConstructedImage = BinaryToImage(Binary)

	Buffer = io.BytesIO()
	ConstructedImage.save(Buffer, "PNG")
	Buffer.seek(0)

	File = discord.File(Buffer, "constructed.png")
	await Interaction.response.send_message(f"Filename: `{FilePath.name}`\nPath: `{FilePath.resolve()}`", file = File)

	Buffer.close()
	ConstructedImage.close()
