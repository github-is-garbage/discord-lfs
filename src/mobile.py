from discord.gateway import DiscordWebSocket

class MobileWebSocket(DiscordWebSocket):
	async def send_as_json(self, Data):
		if Data.get("op") == self.IDENTIFY:
			Block = Data.get("d", {})
			BlockProperties = Block.get("properties", {})

			if BlockProperties.get("browser") is not None:
				BlockProperties["browser"] = "Discord Android"
				BlockProperties["device"] = "Discord Android"

		await super().send_as_json(Data)

DiscordWebSocket.from_client = MobileWebSocket.from_client
