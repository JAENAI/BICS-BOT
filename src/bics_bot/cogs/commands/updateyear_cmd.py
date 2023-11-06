from nextcord import application_command, Interaction
from nextcord.ext import commands

from bics_bot.embeds.logger_embed import LogLevel, LoggerEmbed
from bics_bot.config.server_ids import (
    ROLE_YEAR2_ID,
    ROLE_YEAR3_ID,
    ROLE_ALUMNI_ID,
)


class UpdateYearCmd(commands.Cog):
    """This class represents the command </update>

    The </update> command will allow students to update their current bachelor
    year to the next year. So if they are in `year1`, they will be in `year2`.

    PS This command will face heavy rework during the "AUTHENTICATION update",
    thus is not properly maintained.

    Attributes:
        client: Required by the API, not directly utilized.
    """

    def __init__(self, client):
        self.client = client

    @application_command.slash_command(
        description="Update your bachelor year to the next year",
    )
    async def update(self, interaction: Interaction):
        """
        This method represents the </update> command which allows a student to
        update their current bachelor year to the next year.
        So if they are in `year1`, they will be in `year2`.

        Args:
            interaction: Required by the API. Gives meta information about
              the interaction.
        """
        isAdmin = False
        user = interaction.user
        for role in user.roles:
            if role.name == "Admin":
                isAdmin = True
        if not isAdmin:
            msg = "Sorry, this command is under development and reserved for admins only."
            await interaction.response.send_message(
                embed=LoggerEmbed(msg, LogLevel.WARNING),
                ephemeral=True,
            )
            return

        user = interaction.user
        for role in user.roles:
            if role.name == "Erasmus":
                msg = "This command is only available for full **UniLu** students"
                await interaction.response.send_message(
                    embed=LoggerEmbed(msg, LogLevel.WARNING),
                    ephemeral=True,
                )
                return
        old_role = ""
        new_role = ""
        members = user.guild.members
        for member in members:
            for role in member.roles:
                # if role.name == "Incoming":
                #     old_role = role
                #     new_role = interaction.guild.get_role(ROLE_YEAR1_ID)
                #     await member.remove_roles(role)
                #     await member.add_roles(new_role)
                if role.name == "Year 1":
                    old_role = role
                    new_role = interaction.guild.get_role(ROLE_YEAR2_ID)
                    await member.remove_roles(role)
                    await member.add_roles(
                        interaction.guild.get_role(ROLE_YEAR2_ID)
                    )
                elif role.name == "Year 2":
                    old_role = role
                    new_role = interaction.guild.get_role(ROLE_YEAR3_ID)
                    await member.remove_roles(role)
                    await member.add_roles(
                        interaction.guild.get_role(ROLE_YEAR3_ID)
                    )
                elif role.name == "Year 3":
                    old_role = role
                    new_role = interaction.guild.get_role(ROLE_ALUMNI_ID)
                    await member.remove_roles(role)
                    await member.add_roles(
                        interaction.guild.get_role(ROLE_ALUMNI_ID)
                    )
            # msg = f"Your year role has been updated from {old_role.name} to {new_role.name}"
            # await interaction.response.send_message(
            #     embed=LoggerEmbed("Role Status", msg),
            #     ephemeral=True,
            # )


def setup(client):
    """Function used to setup nextcord cogs"""
    client.add_cog(UpdateYearCmd(client))
