from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from const import channel_id, general
from const.color import EmbedColor
from utils.finder import Finder
from utils.logger import getMyLogger

from .component import CreateTicketButton

if TYPE_CHECKING:
    # import some original class
    from src.bot import Bot

    pass


class Ticket(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.logger = getMyLogger(__name__)

    @commands.command(name="send-ticket")
    @commands.has_role(general.ADMIN_ROLE_ID)
    async def send_ticket(self, ctx: commands.Context):  # type: ignore
        view = discord.ui.View(timeout=None)
        view.add_item(CreateTicketButton())

        embed = discord.Embed(title="運営への問い合わせ", description="ボタンを押すと運営メンバーに直接問い合わせができます。", color=EmbedColor.default)
        finder = Finder(self.bot)
        channel = await finder.find_channel(channel_id.TICKET_CHANNEL_ID, type=discord.TextChannel)

        await channel.send(embed=embed, view=view)
        return


async def setup(bot: "Bot"):
    await bot.add_cog(Ticket(bot))
