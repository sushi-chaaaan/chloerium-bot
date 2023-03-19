from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from const import general
from const.color import EmbedColor
from utils.time import TimeUtils

if TYPE_CHECKING:
    from src.bot import Bot


class Moderation(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @app_commands.command(name="user", description="ユーザー情報を照会できます。")
    @app_commands.guilds(discord.Object(id=general.GUILD_ID))
    @app_commands.describe(target="照会するユーザーを選択してください。(IDの貼り付けもできます)")
    @app_commands.rename(target="ユーザー")
    async def user(
        self,
        interaction: discord.Interaction,
        target: discord.Member | discord.User,
    ):
        await interaction.response.defer()

        embed = user_info(target).set_footer(
            text=f"Commanded by {str(interaction.user)}", icon_url=interaction.user.display_avatar.url
        )
        await interaction.followup.send(embed=embed)
        return


def user_info(target: discord.Member | discord.User) -> discord.Embed:
    avatar_url = (
        target.default_avatar.url
        if target.default_avatar == target.display_avatar
        else target.display_avatar.replace(size=1024, static_format="webp")
    )
    embed = discord.Embed(
        title="ユーザー情報照会結果",
        description=f"対象ユーザー: {target.mention}",
        color=EmbedColor.default.value,
    )
    embed.set_thumbnail(url=avatar_url)
    embed.add_field(
        name="Bot?",
        value=target.bot,
    )
    embed.add_field(
        name="アカウント作成日時",
        value=f"{TimeUtils.dt_to_str(target.created_at)}",
    )
    if isinstance(target, discord.Member):
        joined = TimeUtils.dt_to_str(target.joined_at) if target.joined_at else "取得できませんでした"
        embed.add_field(
            name="サーバー参加日時",
            value=f"{joined}",
        )
        roles = sorted(target.roles, key=lambda role: role.position, reverse=True)
        text = "\n".join([role.mention for role in roles])
        embed.add_field(
            name=f"所持ロール({len(roles)})",
            value=text,
            inline=False,
        )
    else:
        embed.description = f"\N{Warning Sign}このサーバーにいないユーザーです。\n対象ユーザー: {target.mention}"
    return embed
