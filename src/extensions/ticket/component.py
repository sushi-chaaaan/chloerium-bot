import discord
from discord import ui

from const import channel_id, custom_id, general
from utils.logger import getMyLogger
from utils.time import TimeUtils


class CreateTicketButton(ui.Button):  # type: ignore
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.gray,
            label="チケットを作成する",
            custom_id=custom_id.CREATE_TICKET_BUTTON,
            emoji="\N{Thought Balloon}",
        )

    async def callback(self, interaction: discord.Interaction):
        # このButtonは専用コマンドでチケット用TextChannelに送信されるので
        # interaction.channelはTICKET_CHANNEL_IDのTextChannelになる
        if (
            not interaction.channel
            or not isinstance(interaction.channel, discord.TextChannel)
            or interaction.channel.id != channel_id.TICKET_CHANNEL_ID
        ):
            return

        modal = GetTicketNameModal()
        await interaction.response.send_modal(modal)
        await modal.wait()
        if modal.failed:
            return

        ticket_date = TimeUtils.dt_to_str(format="%Y%m%d")
        ticket_name = f"{ticket_date}_{modal.ticket_name.value}"
        ticket_channel: discord.TextChannel = interaction.channel

        mod_mention = f"<@&{general.MODERATOR_ROLE_ID}>"

        thread = await ticket_channel.create_thread(
            name=ticket_name,
            message=None,
            auto_archive_duration=10080,
            type=discord.ChannelType.private_thread,
            invitable=False,
        )
        await interaction.followup.send(f"スレッドを作成しました。\n以降のやり取りはこちらでお願いします。\n{thread.mention}")
        await thread.send(
            f"""
{interaction.user.mention} さん
お問い合わせありがとうございます。
このスレッドでは運営メンバーと直接話し合うことができます。
お困りのことについて教えてください。

{mod_mention}
"""
        )
        return


class GetTicketNameModal(ui.Modal):
    def __init__(self) -> None:
        super().__init__(title="チケット名入力", timeout=None, custom_id=custom_id.GET_TICKET_NAME_MODAL)

        # TODO: placeholder
        self.ticket_name: ui.TextInput = ui.TextInput(  # type: ignore
            label="お問い合わせの内容を簡単に入力してください。(最大30文字)",
            style=discord.TextStyle.short,
            placeholder="例: どのチャンネルに投稿すればいいかわからない",
            required=True,
            max_length=30,
        )
        self.add_item(self.ticket_name)
        self.failed = False

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        self.stop()
        await interaction.followup.send("入力を受け付けました。", ephemeral=True)
        return

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:  # type: ignore
        await interaction.response.defer(ephemeral=True)
        self.stop()
        self.failed = True
        logger = getMyLogger(__name__)
        logger.exception(error)
        await interaction.followup.send("エラーが発生しました。", ephemeral=True)
        return
