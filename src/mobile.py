from discord.gateway import DiscordWebSocket

class MobileWebSocket(DiscordWebSocket):
	async def send_as_json(self, data):
		if data.get("op") == self.IDENTIFY:
			block = data.get("d", {})
			block_properties = block.get("properties", {})

			if block_properties.get("browser") is not None:
				block_properties["browser"] = "Discord Android"
				block_properties["device"] = "Discord Android"

		await super().send_as_json(data)

DiscordWebSocket.from_client = MobileWebSocket.from_client
