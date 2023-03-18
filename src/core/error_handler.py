from typing import TYPE_CHECKING

from discord.ext import commands

from const import log
from utils.logger import getMyLogger

if TYPE_CHECKING:
    # import some original class
    from src.bot import Bot

    pass


class ErrorCatcher(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.logger = getMyLogger(__name__)

    @commands.Cog.listener(name="on_error")
    async def on_error(self, event: str, *args, **kwargs):
        self.logger.exception(log.on_error(event, *args, **kwargs), exc_info=True)
        return

    @commands.Cog.listener(name="on_command_error")
    async def on_command_error(self, ctx: commands.Context, exc: commands.CommandError):  # type: ignore
        await ctx.defer(ephemeral=True)
        self.logger.exception(log.on_command_error(ctx, exc))
        return


async def setup(bot: "Bot"):
    await bot.add_cog(ErrorCatcher(bot))
