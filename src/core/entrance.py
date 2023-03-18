import os
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from const.literal.entrance import join_log, leave_log
from utils.finder import Finder
from utils.time import TimeUtils

if TYPE_CHECKING:
    # import some original class
    from src.bot import Bot

    pass


class Entrance(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.Cog.listener(name="on_member_join")
    async def on_join(self, member: discord.Member):
        msg = join_log(
            joined=TimeUtils.dt_to_str(),
            name=member.name,
            id=member.id,
            mention=member.mention,
            created=TimeUtils.dt_to_str(member.created_at),
            count=member.guild.member_count or -1,
        )
        self.bot.logger.debug(msg)

        finder = Finder(self.bot)
        channel = await finder.find_channel(int(os.environ["ENTRANCE_CHANNEL_ID"]), type=discord.TextChannel)
        await channel.send(msg)
        return

    @commands.Cog.listener(name="on_raw_member_remove")
    async def on_leave(self, payload: discord.RawMemberRemoveEvent):
        finder = Finder(self.bot)
        guild = await finder.find_guild(payload.guild_id)

        msg = leave_log(
            left=TimeUtils.dt_to_str(),
            name=payload.user.name,
            id=payload.user.id,
            mention=payload.user.mention,
            created=TimeUtils.dt_to_str(payload.user.created_at),
            count=guild.member_count or -1,
        )
        self.bot.logger.info(msg)

        channel = await finder.find_channel(int(os.environ["ENTRANCE_CHANNEL_ID"]), type=discord.TextChannel)
        await channel.send(msg)
        return


async def setup(bot: "Bot"):
    await bot.add_cog(Entrance(bot))
