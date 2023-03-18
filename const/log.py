import discord
from discord.ext import commands

APP_COMMAND_LOG_FORMAT = """
[Interaction Command]
Command Name: {command_name}
Guild ID: {guild_id}
Channel ID: {channel_id}
Author ID: {author_id}
Author Name: {author_name}
"""


def app_command_log(interaction: discord.Interaction) -> str:
    return APP_COMMAND_LOG_FORMAT.format(
        command_name=interaction.command.name if interaction.command else "None",
        guild_id=interaction.guild.id if interaction.guild else "None",
        channel_id=interaction.channel.id if interaction.channel else "None",
        author_id=interaction.user.id,
        author_name=interaction.user.name,
    )


COMMAND_LOG = """
[Command]
Command Name: {command_name}
Guild ID: {guild_id}
Channel ID: {channel_id}
Author ID: {author_id}
Author Name: {author_name}
"""


def command_log(ctx: commands.Context) -> str:  # type: ignore
    return COMMAND_LOG.format(
        command_name=ctx.command.name if ctx.command else "None",
        guild_id=ctx.guild.id if ctx.guild else "None",
        channel_id=ctx.channel.id,
        author_id=ctx.author.id,
        author_name=ctx.author.name,
    )


ON_ERROR = """
[ON_ERROR]
Event: {event}
args: {args}
kwargs: {kwargs}
"""


def on_error(event: str, *args, **kwargs) -> str:
    return ON_ERROR.format(
        event=event,
        args=args,
        kwargs=kwargs,
    )


ON_COMMAND_ERROR = """
[ON_COMMAND_ERROR]
Command Name: {command_name}
Guild ID: {guild_id}
Channel ID: {channel_id}
Author ID: {author_id}
Author Name: {author_name}

Exception: {exception}
"""


def on_command_error(ctx: commands.Context, exc: commands.CommandError) -> str:  # type: ignore
    return ON_COMMAND_ERROR.format(
        command_name=ctx.command.name if ctx.command else "None",
        guild_id=ctx.guild.id if ctx.guild else "None",
        channel_id=ctx.channel.id,
        author_id=ctx.author.id,
        author_name=ctx.author.name,
        exception=str(exc),
    )


LOGIN_LOG = """
Logged in as {user} (ID: {id})
Connected to {guilds} guilds
Bot is ready
"""


def login_log(user: discord.ClientUser | None, guild_amount: int) -> str:
    return LOGIN_LOG.format(
        user=user,
        id=user.id if user else "None",
        guilds=str(guild_amount),
    )


JOIN_LOG = """
時刻: {joined}
参加メンバー名: {name} (ID:{id})
メンション: {mention}
アカウント作成時刻: {created}
現在のメンバー数:{count}
"""


def on_member_join(joined: str, name: str, id: int, mention: str, created: str, count: int) -> str:
    return JOIN_LOG.format(
        joined=joined,
        name=name,
        id=str(id),
        mention=mention,
        created=created,
        count=str(count),
    )


LEAVE_LOG = """
時刻: {left}
退出メンバー名: {name} (ID:{id})
メンション: {mention}
アカウント作成時刻: {created}
現在のメンバー数:{count}
"""


def on_member_leave(left: str, name: str, id: int, mention: str, created: str, count: int) -> str:
    return LEAVE_LOG.format(
        left=left,
        name=name,
        id=str(id),
        mention=mention,
        created=created,
        count=str(count),
    )
