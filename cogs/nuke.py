import discord
from discord import Interaction, ui
from discord.ext import commands
from discord.ui import Button

from db.database import nuke_playcounts


# Confirmation View with Buttons
class NukeConfirmationView(ui.View):
    def __init__(self, server_id: str):
        super().__init__()
        self.server_id = server_id

    @discord.ui.button(label="Yes, nuke all playcounts", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: Interaction, button: Button):
        # Call the function to nuke playcounts
        result = nuke_playcounts(self.server_id)

        # Acknowledge the action
        if result:
            await interaction.response.edit_message(
                content="All playcounts have been reset to zero. The wheel will now show all games equally.",
                embed=None,
                view=None
            )
        else:
            await interaction.response.edit_message(
                content="There was a problem resetting the playcounts. Please check logs and report errors or try again.",
                embed=None,
                view=None
            )

    @discord.ui.button(label="No, cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: Interaction, button: Button):
        await interaction.response.edit_message(
            content="Nuke canceled.",
            embed=None,
            view=None
        )


class NukeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command to nuke all playcounts
    @discord.app_commands.command(name="nuke", description="Reset all played counts to zero for a fresh wheel")
    async def nuke(self, interaction: Interaction):
        """Reset all played counts to zero, allowing the wheel to show all games equally."""
        server_id = str(interaction.guild.id)

        # Create the confirmation view
        view = NukeConfirmationView(server_id)

        # Send confirmation message with buttons
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Are you sure you want to nuke all playcounts?",
                description="This will reset the played count for all games to zero, allowing the wheel to show all games equally. Play history will be preserved but ignored. Proceed with caution.",
                color=discord.Color.red()
            ),
            view=view,
            ephemeral=True
        )


# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(NukeCog(bot))