## Error handler cog
## Cog Version: 0.0.1.0

import traceback, discord, sys
from discord.ext import commands

print('Loading error handler cog...')

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        if hasattr(ctx.command, 'on_error'):
            return
        
        ignored = (commands.CommandNotFound, commands.UserInputError)
        error = getattr(error, 'original', error)
        
        if isinstance(error, ignored):
            return
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')
            return
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in DMs.')
                return
            except:
                pass
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Bad arg')
            return
            
        print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

print('Error handler cog loaded!')

async def setup(bot):
    await bot.add_cog(CommandErrorHandler(bot))