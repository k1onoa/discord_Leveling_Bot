import random

import discord
from discord import app_commands
from discord.ext import commands

import database
from config import XP_MAX, XP_MIN, xp_for_level


class Leveling(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or message.guild is None:
            return

        amount = random.randint(XP_MIN, XP_MAX)
        new_level = await database.add_xp(message.guild.id, message.author.id, amount)

        if new_level is not None:
            await message.channel.send(
                f"🎉 {message.author.mention} 님이 **레벨 {new_level}** 을 달성했습니다!"
            )

    @app_commands.command(name="레벨", description="내 레벨과 XP를 확인해요")
    async def level(self, interaction: discord.Interaction) -> None:
        xp, level = await database.get_user(interaction.guild_id, interaction.user.id)
        need = xp_for_level(level)
        await interaction.response.send_message(
            f"레벨 **{level}** · XP **{xp} / {need}**", ephemeral=True
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Leveling(bot))
