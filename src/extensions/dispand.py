from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from dispander import dispand

from utils.logger import getMyLogger

if TYPE_CHECKING:
    # import some original class
    from src.bot import Bot

    pass


class Dispander(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.logger = getMyLogger(__name__)

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id:  # type: ignore
            return

        try:
            extracted = await dispand(message)
        except Exception as e:
            self.logger.error(e)
            extracted = []

        if extracted is None or extracted == []:
            return

        for fragment in extracted:
            view = discord.ui.View(timeout=None)
            view.add_item(
                discord.ui.Button(
                    label="元のメッセージ",
                    style=discord.ButtonStyle.url,
                    url=fragment["jump_url"],
                )
            )

            try:
                await message.channel.send(
                    embeds=fragment["embeds"][:10],
                    view=view,
                )
            except Exception as e:
                self.logger.error(e, stack_info=True)
        return


async def setup(bot: "Bot"):
    await bot.add_cog(Dispander(bot))
