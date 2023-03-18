import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from const import literal
from const.color import EmbedColor
from db.redis import UnarchiveRedis
from utils.finder.finder import Finder
from utils.logger import getMyLogger

if TYPE_CHECKING:
    # import some original class
    from src.bot import Bot

    pass


class Thread(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.logger = getMyLogger(__name__)

    group = app_commands.Group(
        name="unarchive",
        description="アーカイブ自動解除機能",
        guild_ids=[int(os.environ["GUILD_ID"])],
    )

    @commands.Cog.listener("on_raw_thread_update")
    async def handle_thread_archive(self, payload: discord.RawThreadUpdateEvent):
        thread = await self.get_thread_obj(payload)
        self.logger.debug(f"Thread.archived: {thread.archived}, Thread.locked: {thread.locked}")
        # archived=True: 有効期限切れによるCloseなのでUnarchiveする
        # Thread.archived: True, Thread.locked: False
        # ↓ Unarchive thread
        # Thread.archived: False, Thread.locked: False
        # -----------------
        # locked=True: ユーザーによる意図的なCloseなのでUnarchiveしない
        # Thread.archived: False, Thread.locked: True
        # -----------------
        # 先日のAPI仕様変更でarchivedとlockedが独立したので、どちらも同時にTrueになることはない
        # https://discord.com/developers/docs/change-log#update-to-locked-threads
        if not (thread.archived and not thread.locked):
            return

        async with UnarchiveRedis() as redis:
            if not await redis.is_target(thread.id):
                return

        try:
            await thread.edit(archived=False)
        except discord.Forbidden as e:
            self.logger.exception(literal.FORBIDDEN, exc_info=e)
        except discord.HTTPException as e:
            self.logger.exception(literal.FAILED_TO_UNARCHIVE, exc_info=e)
        return

    @group.command(name="on", description="アーカイブ自動解除を有効にする")
    @app_commands.guild_only()
    async def unarchive_on(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        if not isinstance(interaction.channel, discord.Thread):
            await interaction.followup.send("このコマンドはスレッド内で実行してください。", ephemeral=True)
            return

        toggled_length = await self.toggle_unarchive(interaction.channel.id, on=True)
        match toggled_length:
            case 1:
                res = "アーカイブ設定を有効にしました。"
            case 0:
                res = "既にアーカイブ設定が有効になっています。"
            case _:
                res = "予期せぬエラーが発生しました。"

        await interaction.followup.send(res, ephemeral=True)

    @group.command(name="off", description="アーカイブ自動解除を無効にする")
    @app_commands.guild_only()
    async def unarchive_off(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        if not isinstance(interaction.channel, discord.Thread):
            await interaction.followup.send("このコマンドはスレッド内で実行してください。", ephemeral=True)
            return

        toggled_length = await self.toggle_unarchive(interaction.channel.id, on=False)
        match toggled_length:
            case 1:
                res = "アーカイブ設定を無効にしました。"
            case 0:
                res = "既にアーカイブ設定が無効になっています。"
            case _:
                res = "予期せぬエラーが発生しました。"

        await interaction.followup.send(res, ephemeral=True)

    @group.command(name="status", description="このスレッドのアーカイブ自動解除の設定を表示する")
    @app_commands.guild_only()
    async def unarchive_status(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        if not isinstance(interaction.channel, discord.Thread):
            await interaction.followup.send("このコマンドはスレッド内で実行してください。", ephemeral=True)
            return

        async with UnarchiveRedis() as redis:
            is_already_target = await redis.is_target(interaction.channel.id)

        res = "このスレッドはアーカイブ自動解除の対象です。" if is_already_target else "このスレッドはアーカイブ自動解除の対象ではありません。"
        await interaction.followup.send(res, ephemeral=True)
        return

    @group.command(name="list", description="アーカイブ自動解除の対象のスレッドを表示する")
    @app_commands.guild_only()
    async def unarchive_list(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        async with UnarchiveRedis() as redis:
            targets = await redis.get_targets()

        if not targets or targets == ():
            embed = discord.Embed(
                title="アーカイブ自動解除の対象のスレッド",
                color=EmbedColor.default,
                description="アーカイブ自動解除の対象のスレッドはありません。",
            )
        else:
            embed = discord.Embed(
                title="アーカイブ自動解除の対象スレッド",
                color=EmbedColor.default,
            )
            embed.add_field(
                name="対象スレッド",
                value="\n".join([f"<#{target}>" for target in targets]),
            )

        await interaction.followup.send(embed=embed, ephemeral=True)
        return

    async def toggle_unarchive(self, thread_id: int, on: bool):
        async with UnarchiveRedis() as redis:
            if on:
                return await redis.add_target(thread_id)
            else:
                return await redis.remove_target(thread_id)

    async def get_targets(self) -> tuple[int, ...]:
        async with UnarchiveRedis() as redis:
            return await redis.get_targets()

    async def get_thread_obj(self, payload: discord.RawThreadUpdateEvent):
        if payload.thread:
            return payload.thread
        else:
            finder = Finder(self.bot)
            return await finder.find_channel(payload.thread_id, discord.Thread)


async def setup(bot: "Bot"):
    await bot.add_cog((Thread(bot)))
