# DiscordLFS

Encodes files into binary string data which is then encoded into `.png` images where black pixels are 1's and white pixels are 0's.\
These images are then uploaded to Discord one by one to allow essentially unlimited file storage as long as the message chunks remain.

Not an original idea. I saw [this](https://www.youtube.com/watch?v=eOuephDbkJQ) video and wanted to recreate it for myself :]

## Features

- Runs off slash commands
- Encodes messages for easy downloading, only main message link is required to download
- The bot will be shown as online on mobile because why not
- Slower than hell because I'm bad at python

## Setup

1. `pip install -r requirements.txt`
2. Create a `.env` file in the `src` folder
3. Add the line `BOT_TOKEN=(your bot token here)` to the `.env`
4. Add the line `GUILD_ID=(your guild ID here)` to the `.env`
5. `python3 src/main.py`
6. Profit (Use the bot's slash commands)
