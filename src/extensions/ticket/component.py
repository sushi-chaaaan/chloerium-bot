import discord
from discord import ui

from const import channel_id, custom_id
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
        await interaction.response.defer(ephemeral=True)

        # このButtonは専用コマンドでチケット用TextChannelに送信されるので
        # interaction.channelはTICKET_CHANNEL_IDのTextChannelになる
        if (
            not interaction.channel
            or not isinstance(interaction.channel, discord.TextChannel)
            or interaction.channel.id != channel_id.TICKET_CHANNEL_ID
        ):
            return

        ticket_channel: discord.TextChannel = interaction.channel
        ticket_date = TimeUtils.dt_to_str(format="%m%d")
        # TODO: Modalでチケット名を入力できるようにする
        ticket_name = f"{ticket_date}-ModalResult"

        await ticket_channel.create_thread(
            name=ticket_name,
            message=None,
            auto_archive_duration=10080,
            type=discord.ChannelType.private_thread,
            invitable=False,
        )
        return


class GetTicketNameModal(ui.Modal):
    def __init__(self) -> None:
        super().__init__(title="チケット名入力", timeout=None, custom_id=custom_id.GET_TICKET_NAME_MODAL)
