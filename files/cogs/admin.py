## Admin cog
## Cog Version: 0.0.4.4


import discord, pickledb, time, datetime, asyncio, platform
from discord.ext import commands
from files.shared import logger, is_botadmin, is_me

print('Loading admin cog...')

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db

    @commands.command(name='botadmin', aliases=['ba'])
    @is_botadmin()
    @logger()
    async def botadmin(self, ctx, action:str = None, user:discord.User = None):
        """Bot admin only command. Add or remove bot admins from the list, or returns the list. Usage: botadmins [add/remove/list] [mention user]"""
        if action == None:
            await ctx.channel.send('You must input an action to add/remove from the bot admin list. Usage: botadmins [add/remove] [mention user]')
            return
        if user == None:
            if action == 'list':
                pass
            else:
                await ctx.channel.send('You must input a user to add/remove from the bot admin list. Usage: botadmins [add/remove] [mention user]')
                return
        else:
            uid = user.id
        if action == 'list':
            x = self.db.get('botadmins')
            admins = []
            for uid in x:
                u = self.bot.get_user(uid)
                try:
                    if u.name == None:
                        pass
                    else:
                        if str(u.discriminator) == '0':
                            admins.append(f'{u.name} ({uid})\n')
                        else:
                            admins.append(f'{u.name}#{u.discriminator} ({uid})\n')
                except Exception as e:
                    print(f'Error getting user data for UID {uid}... or another error has occured: {e}')
                    pass
            formatted = "".join(admins)
            #for a in admins:
            #    formatted = formatted.join(f"{a}\n")
            await ctx.channel.send(f'Current bot admins: ```{formatted}```')
        elif action == 'add':
            try:
                x = self.db.get('botadmins')
                if uid in x:
                    await ctx.channel.send('This user is already a bot admin!')
                    return
                x.append(uid)
                self.db.set('botadmins', x)
                self.db.dump()
            except Exception as e:
                await ctx.channel.send(f'Error while adding user to list: {e}')
            else:
                await ctx.channel.send(f'Successfully added {user} ({uid}) to the bot admin list')
        elif action == 'remove':
            if uid == 143183268571774976:
                await ctx.channel.send('You cannot remove the bot developer from the bot admin list.')
                return
            try:
                x = self.db.get('botadmins')
                if uid not in x:
                    await ctx.channel.send('This user is not a bot admin!')
                    return
                x.remove(uid)
                self.db.set('botadmins', x)
                self.db.dump()
            except Exception as e:
                await ctx.channel.send(f'Error while removing user from list: {e}')
            else:
                await ctx.channel.send(f'Successfully removed {user} ({uid}) from the bot admin list')
        return

    @commands.command()
    @is_botadmin()
    @logger()
    async def save(self, ctx):
        """Bot admin only command. Writes the PickleDB database from memory to the data file."""
        try:
            self.db.dump()
        except Exception as e:
            await ctx.channel.send(f'Uh oh! There was a problem saving the data! Error: {e}')
        else:
            await ctx.channel.send('Successfully saved the database!')
        return

    @commands.command(name='eval', aliases=['execute', 'exec', 'evaluate', 'py', 'python'])
    @is_botadmin()
    @logger()
    async def eval(self, ctx, *, arg:str = None):
        """Evaluate Python code. Use printd() to print to Discord. Usage: eval [code]"""
        if arg == None:
            await ctx.channel.send('You must input code to evaluate')
            return
        if "time.sleep(" in arg:
            await ctx.channel.send('You cannot use `time.sleep()` as it is blocking code.')
            return
        print(f'Running eval command code:\n{arg}')
        global dresponse
        dresponse = []
        def printd(x:str = None): ## function usable inside your eval code to send a given variable or string to discord as a response 
            if x != None:
                global dresponse
                dresponse.append(x)
                print(f'message added to response queue: {x}')
        try:
            x = exec(arg)
        except Exception as e:
            await ctx.channel.send(f'Error: `{e}`')
        else:
            if len(dresponse) > 0:
                for message in dresponse:
                    await ctx.channel.send(message)
            if 'printd' in arg:
                await ctx.message.reply("Executed successfully")
            else:
                await ctx.message.reply("Executed successfully (tip: use printd() to print to Discord chat)")
        return

    @commands.command()
    @is_botadmin()
    @logger()
    async def loadcog(self, ctx, cog:str = None):
        """Bot admin only command. Loads a cog. Usage: loadcog [cog]"""
        if cog == None:
            await ctx.channel.send('You must input a cog to load. Command usage: loadcog [cog]')
            return
        try:
            await self.bot.load_extension(cog)
        except Exception as e:
            await ctx.channel.send(f'Error loading cog: {e}')
        else:
            await ctx.channel.send('Loaded cog')

    @commands.command()
    @is_botadmin()
    @logger()
    async def unloadcog(self, ctx, cog:str = None):
        """Bot admin only command. Unloads a cog. Usage: unloadcog [cog]"""
        if cog == None:
            await ctx.channel.send('You must input a cog to unload. Command usage: unloadcog [cog]')
            return
        await self.bot.unload_extension(cog)
        await ctx.channel.send('Unloaded cog')

    @commands.command()
    @is_botadmin()
    @logger()
    async def unloadcogs(self, ctx):
        """Bot admin only command. Unloads all cogs."""
        el = []
        for e in self.bot.extensions:
            el.append(e)
        for e in el:
            await self.bot.unload_extension(e)
        await ctx.channel.send('Unloaded cogs')

    @commands.command(name='reloadcogs', aliases=['rc'])
    @is_botadmin()
    @logger()
    async def reloadcogs(self, ctx):
        """Bot admin only command. Reloads cogs."""
        print('Reloading all currently loaded cogs')
        m = await ctx.channel.send('Reloading cogs...')
        botexts = []
        for e in self.bot.extensions:
            botexts.append(e)
        print(f'ext list: {botexts}')
        for ext in botexts:
            await self.bot.reload_extension(ext)
        await m.edit(content='Reloaded cogs')
        return

    @commands.command()
    @logger()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount:int = 10):
        """Requires manage message permissions. Deletes n amount of messages (defaults to 10) from the channel. Usage: clear [n]"""
        try:
            await ctx.channel.purge(limit=amount+1)
        except discord.Forbidden:
            await ctx.channel.send('I am missing `Manage Messages` permission, cannot clear messages.')
            return
        except Exception as e:
            print('Error while clearing messages')
            await ctx.channel.send('Error while clearing messages. Report this to the bot developer if the problem persists.')
            return
        else:
            cm = await ctx.channel.send(f'Cleared {amount} messages')
            await asyncio.sleep(1.8)
            await cm.delete()

    @commands.command(name='resync', aliases=['rs'])
    @is_botadmin()
    @logger()
    async def resync(self, ctx):
        """Bot admin only command. Resyncs interactions to Discord."""
        print('Resyncing interactions...')
        m = await ctx.channel.send('Resyncing interactions...')
        await self.bot.sync_commands()
        await m.edit(content='Resync complete')
        return

print('Adminstrative commands loaded')

async def setup(bot):
    await bot.add_cog(Admin(bot))