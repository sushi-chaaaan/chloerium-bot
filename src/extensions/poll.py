from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from const.color import EmbedColor
from const.literal.error import POLL_TOO_MANY_OPTIONS
from utils.io import read_json

if TYPE_CHECKING:
    from src.bot import Bot


class Poll(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @commands.command(name="poll")
    @commands.guild_only()
    async def poll(self, ctx: commands.Context, title: str, *select: str):  # type: ignore
        # 1メッセージには20個までしかリアクションがつけられない
        if (options := len(select)) > 20:
            await ctx.reply(POLL_TOO_MANY_OPTIONS)
            return

        emoji_dict = read_json(r"const/poll_emoji.json")

        # select配列が空であればyes or noの投票と判断
        if not select:
            option = [
                {"name": emoji_dict["0"], "value": "はい"},
                {"name": emoji_dict["1"], "value": "いいえ"},
            ]
        else:
            option = [{"name": emoji_dict[str(i)], "value": select[i]} for i in range(options)]

        embed = discord.Embed(
            color=EmbedColor.default.value,
            title=title,
        )
        embed.set_author(name="投票")
        for opt in option:
            embed.add_field(**opt)

        msg = await ctx.send(embeds=[embed])
        for e in [d["name"] for d in option]:
            await msg.add_reaction(e)
        return


async def setup(bot: "Bot"):
    await bot.add_cog(Poll(bot))
