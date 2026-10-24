import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import database

load_dotenv()

EXTENSIONS = [
    "cogs.leveling",
]


class LevelBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self) -> None:
        await database.init_db()
        for ext in EXTENSIONS:
            await self.load_extension(ext)
        await self.tree.sync()

    async def on_ready(self) -> None:
        print(f"로그인 성공!: {self.user} (ID: {self.user.id})")


bot = LevelBot()

if __name__ == "__main__":
    token = os.getenv("TOKEN")
    if not token:
        raise SystemExit(".env 파일에 TOKEN 을 입력해주세요")
    bot.run(token)
