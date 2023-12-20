## Fun cog
## Cog Version: 0.0.1.0


import discord, pickledb, time, datetime, asyncio, platform, random
from discord.ext import commands as cmds
from files.shared import logger, is_botadmin

print('Loading fun cog...')

class Fun(cmds.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @cmds.command(name='8ball', aliases=['8b', '8-ball'])
    @logger()
    async def _8ball(self, ctx, *, question:str = None):
        """Ask the magic 8 ball a question. Usage: 8ball [question]"""
        if question == None:
            await ctx.channel.send('You must input a question to ask the 8 ball. Usage: 8ball [question]')
            return
        if '@everyone' in ctx.message.content:
            pass
        elif '@here' in ctx.message.content:
            pass
        else:
            responses = ['As I see it, yes.',
                        'Ask again later.',
                        'Better not tell you now.',
                        'Cannot predict now.',
                        'Concentrate and ask again.',
                        'Don’t count on it.',
                        'It is certain.',
                        'It is decidedly so.',
                        'Most likely.',
                        'My reply is no.',
                        'My sources say no.',
                        'Outlook not so good.',
                        'Outlook good.',
                        'Reply hazy, try again.',
                        'Signs point to yes.',
                        'Very doubtful.',
                        'Without a doubt.',
                        'Yes.',
                        'Yes – definitely.',
                        'You may rely on it.'
                        ]
            embed=discord.Embed(title="Magic 8 Ball", color=0x000000)
            embed.add_field(name="Question", value=f"```{question}```", inline=False)
            embed.add_field(name="Answer", value=f"```{random.choice(responses)}```", inline=False)
            await ctx.channel.send(embed=embed)

print('Fun commands loaded')

async def setup(bot):
    await bot.add_cog(Fun(bot))