## Default cog
## Cog Version: 0.0.2.3


import discord, asyncio, aiohttp
from discord.ext import commands as cmds
from files.shared import logger, is_botadmin, GuildData

print('Loading default commands...')

class MainCommands(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
        self.version = bot.version

    @cmds.hybrid_command(name='test')
    @logger()
    async def test(self, ctx):
        """Test command to see if the bot is online and responding properly"""
        await ctx.reply(f'Hello <@!{ctx.author.id}>!')
        return

    @cmds.hybrid_command(name='version', aliases=['ver', 'v', 'botver', 'botversion'])
    @logger()
    async def version(self, ctx):
        """Returns current bot version"""
        await ctx.reply(f'Current version: `{self.version}`')
        return

    @cmds.hybrid_command(name='ping')
    @logger()
    async def ping(self, ctx):
        """Returns bot ping."""
        ping = round(self.bot.latency * 1000)
        await ctx.reply(f'Ping: {ping}ms')

    @cmds.command(name='prefix')
    @logger()
    async def prefix(self, ctx, p:str = None):
        """Get or set the current prefix. You must have Manage Server permissions to change the prefix."""
        gid = str(ctx.guild.id)
        if p == None:
            prefixes = self.db.get('prefixes')
            prefix = prefixes[gid]
            await ctx.channel.send(f'Current prefix for the guild **{ctx.guild.name}**: `{prefix}`')
            return
        else:
            hasperm = False
            for role in ctx.author.roles:
                if role.permissions.administrator == True:
                    hasperm = True
                if role.permissions.manage_guild == True:
                    hasperm = True
            if hasperm == True:
                self.db.dpop('prefixes', gid)
                self.db.dadd('prefixes', [gid, p])
                self.db.dump()
                await ctx.channel.send(f'Prefix set to `{p}`!')
                return
            else:
                await ctx.channel.send(f"Error: You need `Manage Server` to change a guild's prefix.")
                return
        return
    
    @cmds.command(name='shutdown', aliases=['close', 'stop', 'stopbot'])
    @is_botadmin()
    @logger()
    async def shutdown(self, ctx):
        """Bot admin only command. Performs a complete shutdown of the bot. It should come back online in a few moments if 24/7 hosting is available."""
        await ctx.channel.send("Shutting down!")
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="Shutting down..."))
        await self.bot.close()

print('Default commands loaded')

async def setup(bot):
    await bot.add_cog(MainCommands(bot))