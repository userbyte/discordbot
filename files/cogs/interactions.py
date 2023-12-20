## Interactions cog
## Cog Version: 0.0.1.1


import discord
from discord import app_commands, ui
from discord.ext import commands
from typing import Optional
from files.shared import logger, is_botadmin

print('Loading interactions commands...')

class Interactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @app_commands.command()
    @logger()
    async def hello(self, interaction: discord.Interaction):
        """Says hello!"""
        await interaction.response.send_message(f'Hi, {interaction.user.mention}')

    @app_commands.command()
    @app_commands.describe(
        first_value='The first value you want to add something to',
        second_value='The value you want to add to the first value',
    )
    async def add(self, interaction: discord.Interaction, first_value: int, second_value: int):
        """Adds two numbers together."""
        await interaction.response.send_message(f'{first_value} + {second_value} = {first_value + second_value}')

    @app_commands.command()
    @app_commands.rename(text_to_send='text')
    @app_commands.describe(text_to_send='Text to send in the current channel')
    async def send(self, interaction: discord.Interaction, text_to_send: str):
        """Sends the text into the current channel."""
        await interaction.response.send_message(text_to_send)

    @app_commands.command()
    @app_commands.describe(member='The member you want to get the joined date from; defaults to the user who uses the command')
    async def joined(self, interaction: discord.Interaction, member: Optional[discord.Member] = None):
        """Gets guild join date of a user."""
        member = member or interaction.user
        await interaction.response.send_message(f'{member} joined {discord.utils.format_dt(member.joined_at)}')

print('Interactions loaded')

async def setup(bot):
    await bot.add_cog(Interactions(bot))