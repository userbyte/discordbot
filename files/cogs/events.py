## Events hook cog
## Cog Version: 0.0.2.3


import discord, time, datetime, asyncio
from discord.ext import commands
from files.shared import logger, is_botadmin
from colored import fg, attr, stylize, bg

print('Registering event listeners...')

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.t0 = bot.t0

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            print(f'Guild joined: {guild.name} owned by {guild.owner.name}#{guild.owner.discriminator} ({guild.owner.id})')
        except UnicodeEncodeError:
            print(f'Guild joined: {guild.name.id} owned by {guild.owner.id}')
        self.db.dadd('prefixes', [guild.id, '$'])

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        try:
            print(f'Guild removed: {guild.name} owned by {guild.owner.name}#{guild.owner.discriminator} ({guild.owner.id})')
        except UnicodeEncodeError:
            print(f'Guild removed: {guild.name.id} owned by {guild.owner.id}')
        self.db.dpop('prefixes', guild.id)

    @commands.Cog.listener()
    async def on_ready(self):
        global isConnected
        try:
            isConnected
        except NameError:
            await self.bot.sync_commands() # needs to be done after bot is ready so guilds list is populated
            isConnected = 1
            t1 = time.time()
            total = t1 - self.t0
            total = round(total)
            print(stylize(f'Bot ready!', fg(2)))
            print(stylize(f'Logged in as {self.bot.user}', fg(2)))
            print(stylize(f'Loading time: {total} seconds', fg(8)))
            print(stylize(f'WS latency: {round(self.bot.latency * 1000)}ms', fg(8)))
            print(stylize(f'Currently serving {len(self.bot.guilds)} guilds', fg(8)))
            print(stylize(f'{len(self.bot.extensions)} modules loaded', fg(8)))
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f"with new code!"))
        else:
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f"with new code!"))
            print(stylize(f'Reconnected', fg(2)))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            print(f'{member} has joined {member.guild}')
        except UnicodeEncodeError:
            print(f'{member.id} has joined {member.guild.id}')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            print(f'{member} has left {member.guild}')
        except UnicodeEncodeError:
            print(f'{member.id} has left {member.guild.id}')

print('Event listeners registered')

async def setup(bot):
    await bot.add_cog(Events(bot))