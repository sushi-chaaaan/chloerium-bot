from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from const import channel_id
from utils.finder import Finder

if TYPE_CHECKING:
    # import some original class
    from src.bot import Bot

    pass


class DM(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def handle_direct_message(self, message: discord.Message):
        if self.bot.user.id == message.author.id or not isinstance(message.channel, discord.DMChannel):  # type: ignore
            return

        finder = Finder(self.bot)
        channel = await finder.find_channel(channel_id.DM_TRANSFER_CHANNEL_ID, discord.TextChannel)

        await channel.send("HOGE")
        return


async def setup(bot: "Bot"):
    await bot.add_cog(DM(bot))
