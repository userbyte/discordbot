# functions and shit shared across various files of the bot

import time, datetime, platform
from discord.ext import commands

def initialize_db(self):
    print('Initializing database...')
    if self.db.get('botadmins') == False:
        self.db.set('botadmins', [143183268571774976])
        self.db.dump()
    if self.db.get('guild_data') == False:
        self.db.set('guild_data', {})
        self.db.dump()
    print('Done')

class GuildData:
    def __init__(self, cogself, guild_id):
        self.db = cogself.db
        self.guild_id = str(guild_id)
        guild_data = self.db.get('guild_data')
        try:
            guild_data[self.guild_id]
        except KeyError:
            # no guild data in db yet, add it
            self.db.dadd('guild_data', [self.guild_id, {}])

    def __repr__(self):
        guild_data = self.db.get('guild_data')
        return f'{guild_data[self.guild_id]}'

    def __str__(self):
        guild_data = self.db.get('guild_data')
        return f'{guild_data[self.guild_id]}'

    def set(self, key, val):
        guild_data = self.db.get('guild_data')
        guild_data[self.guild_id][key] = val
        self.db.set('guild_data', guild_data)
        self.db.dump()
        return 1
        # self.db.dset('guild_data', [key, val])

    def get(self, key):
        print(f'GuildData.get({key=})')
        guild_data = self.db.get('guild_data')
        val = guild_data[self.guild_id][key]
        return val

def get_prefix(client,message):
    prefixes = client.db.get('prefixes')
    cfg = client.cfg
    gid = str(message.guild.id)
    try:
        prefix = prefixes[gid]
    except TypeError:
        client.db.dcreate('prefixes')
        client.db.dadd('prefixes', [gid, cfg['defaultprefix']])
        client.db.dump()
        prefix = cfg['defaultprefix']
    except KeyError:
        client.db.dadd('prefixes', [gid, cfg['defaultprefix']])
        client.db.dump()
        prefix = cfg['defaultprefix']
    return prefix

def ampmformat(hhmmss):
    ampm = hhmmss.split (":")
    if (len(ampm) == 0) or (len(ampm) > 3):
        return hhmmss
    hour = int(ampm[0]) % 24
    isam = (hour >= 0) and (hour < 12)
    if isam:
        ampm[0] = ('12' if (hour == 0) else "%2d" % (hour))
    else:
        ampm[0] = ('12' if (hour == 12) else "%2d" % (hour-12))
    if int(ampm[0]) < 10:
        ampm[0] = str(int(ampm[0]))
    return ':'.join(ampm) + (' AM' if isam else ' PM')

def get_dt():
    """Get current date and time."""
    mylist = []
    today = datetime.date.today()
    mylist.append(today)
    if platform.system() == 'Linux':
        date = today.strftime('%b %-d, %Y')
    if platform.system() == 'Windows':
        date = today.strftime('%b %#d, %Y')
    else:
        date = today.strftime('%b %-d, %Y')
    m = ampmformat(time.strftime("%H:%M:%S"))
    dt = f'{date} @ {m}'
    return dt

def write_to_log(l):
    try:
        dt = get_dt()
        with open("logs/bot.log", "a") as f:
            f.write(f"{dt} -   {l}\n")
    except UnicodeEncodeError:
        print(f'Error writing to log. Content contains an un-writable unicode char.')
    except Exception as e:
        print(f'Error writing "{l}" to log. Error: {e}')

def logger():
    def predicate(ctx):
        if 'help' in ctx.message.content:
            pass
        else:
            try:
                NoneType = type(None)
                if isinstance(ctx.guild, NoneType):
                    dt = get_dt()
                    print(f'Command "{ctx.command}" used by {ctx.author.name} ({ctx.author.id}) in DMs at {dt}: {ctx.message.content}')
                    write_to_log(f'Command "{ctx.command}" used by {ctx.author.name} ({ctx.author.id}) in DMs at {ctx.message.created_at}: {ctx.message.content}')
                elif not isinstance(ctx.interaction, NoneType):
                    # if this command was an Interaction
                    dt = get_dt()
                    print(f'Slash command "{ctx.command}" used by {ctx.author.name} ({ctx.author.id}) in {ctx.guild.name} at {dt}')
                    write_to_log(f'Slash command "{ctx.command}" used by {ctx.author.name} ({ctx.author.id}) in {ctx.guild.name} at {ctx.message.created_at}')
                else:
                    dt = get_dt()
                    print(f'Command "{ctx.command}" used by {ctx.author.name} ({ctx.author.id}) in {ctx.guild.name} at {dt}: {ctx.message.content}')
                    write_to_log(f'Command "{ctx.command}" used by {ctx.author.name} ({ctx.author.id}) in {ctx.guild.name} at {ctx.message.created_at}: {ctx.message.content}')
            except UnicodeEncodeError:
                dt = get_dt()
                print(f'Command "{ctx.command}" used by (CONTAINS UNICODE CHAR) at {dt}: (CONTAINS UNICODE CHAR)')
                write_to_log(f'Command "{ctx.command}" used by {ctx.author.name} ({ctx.author.id}) in {ctx.guild.name} at {ctx.message.created_at}: {ctx.message.content}')
        return 1
    return commands.check(predicate)

def is_botadmin():
    async def predicate(ctx):
        botadmins = ctx.cog.db.get('botadmins')
        if ctx.author.id in botadmins:
            return True
        else:
            if 'help' in ctx.message.content:
                pass
            else:
                await ctx.channel.send(f'You are not permitted to use the command: `{ctx.command}`')
    return commands.check(predicate)

def is_me():
    def predicate(ctx):
        return ctx.message.author.id == 143183268571774976
    return commands.check(predicate)   