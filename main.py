## discordbot
## 9/29/2023
## Written by userbyte
## Description: Generic Discord bot to be used as a template for new bots

import discord, logging, time, os, json, asyncio, aiohttp, pickledb, toml
from discord.ext import commands
from colored import fg, attr, stylize, bg
from files.shared import get_prefix, initialize_db

t0 = time.time()
debugmode = 0
botname = 'discordbot'
botvernum = '0.0.0.0'
botverfull = f'{botname} {botvernum}'

print(f'''
{bg(8)+fg(15)+attr("bold")}     _ _                       _ _           _   {attr("reset")}
{bg(8)+fg(15)+attr("bold")}    | (_)                     | | |         | |  {attr("reset")}
{bg(8)+fg(15)+attr("bold")}  __| |_ ___  ___ ___  _ __ __| | |__   ___ | |_ {attr("reset")}
{bg(8)+fg(15)+attr("bold")} / _` | / __|/ __/ _ \| '__/ _` | '_ \ / _ \| __|{attr("reset")}
{bg(8)+fg(15)+attr("bold")}| (_| | \__ \ (_| (_) | | | (_| | |_) | (_) | |_ {attr("reset")}
{bg(8)+fg(15)+attr("bold")} \__,_|_|___/\___\___/|_|  \__,_|_.__/ \___/ \__|{attr("reset")}''')

print(stylize(f'discord.py version: {discord.__version__}', fg(8)))
print(stylize(f'Bot version: {botvernum}', fg(8)))
print(stylize(f'Starting {botname}...', fg(3)))

logging.basicConfig(level=logging.WARNING)

global cfg
global token
global defaultprefix
def load_config():
    global cfg
    global token
    global defaultprefix
    cfg_dir = './files/cfg'
    print(stylize(f'Loading config file ({cfg_dir}/config.toml)...', fg(5)))
    if not os.path.exists('files'):
        # create files dir if not exist
        os.mkdir('files')
    if not os.path.exists(f'{cfg_dir}'):
        # create cfg dir if not exist
        os.mkdir(f'{cfg_dir}')
    try:
        try:
            with open(f'{cfg_dir}/config.toml', 'r') as f:
                cfg = toml.load(f)
        except Exception as e:
            print('Config file missing!')
            raise FileNotFoundError(2, os.strerror(2), f'{cfg_dir}/config.toml')
        else:
            token = cfg['token']
            defaultprefix = cfg['defaultprefix']
    except Exception as e:
        print(stylize(f'One of the config values is incorrect or the config file is missing! (err: {e})', fg(1)))
        print(stylize('You need to create a config!', fg(5)))
        cfg = {
          "token": input('Enter your bot token: '),
          "defaultprefix": input('Enter the default command prefix you want: ')
        }
        token = cfg['token']
        defaultprefix = cfg['defaultprefix']
        print(stylize(f'Saving config to {os.getcwd()}{cfg_dir}/config.toml...', fg(5)))
        with open(f'{cfg_dir}/config.toml', 'w') as f:
            toml.dump(cfg, f, encoder=None)
        print(stylize('Config saved!', fg(2)))
        print(stylize('Successfully loaded config!', fg(2)))
    else:
        print(stylize('Successfully loaded config!', fg(2)))

load_config()

# ------ Var Definitions ------

global isConnected

DEV_SYNC_ONLY = False
DEV_GUILD_ID = 260166835440320515

class Bot(commands.Bot):
    async def sync_commands(self):
        cl = []
        for command in self.tree.walk_commands():
            cl.append(f'{command.name} ({command.callback.__qualname__})')
        print(f'Commands in tree: {cl}')
        if DEV_SYNC_ONLY:
            print('Syncing commands to dev guild...')
            DEV_GUILD = discord.Object(id=DEV_GUILD_ID) # guild to sync commands to for development testing
            self.tree.copy_global_to(guild=DEV_GUILD)
            await self.tree.sync(guild=DEV_GUILD)
            print('Sync complete!')
        else:
            print(f'Syncing commands to all guilds ({len(self.guilds)})...')
            for g in self.guilds:
                print(f'syncing to {g}')
                self.tree.copy_global_to(guild=g)
                await self.tree.sync(guild=g)
            print('Sync complete!')

    async def setup_hook(self):
        # print('~ running setup hook')
        await load_cogs()
        initialize_db(self)
        # print('~ setup hook complete')

    async def async_cleanup(self):
        print(stylize('Cleaning up...', fg(8)))
        async with aiohttp.ClientSession() as session:
            try:
                self.db.dump()
            except Exception as e:
                print(stylize(f'Error while saving database!: {e}', fg(1)))
                return
            else:
                print(stylize('Database successfully saved', fg(2)))
            print(stylize('Changing bot status to: OFFLINE', fg(5)))
            if super() == None:
                print("Bot not ready")
                print(stylize('Shutdown triggered before bot ready', fg(1)))
            else:
                await super().change_presence(status=discord.Status.offline)
            await session.close()
            await asyncio.sleep(1.5)
            # exit()
            print(stylize('Cleanup complete!', fg(2)))

    async def close(self):
        print(stylize('\nBot shutdown triggered!', fg(3)))
        await self.async_cleanup()
        print(stylize('Stopping...', fg(3)))
        await super().close()
        print(stylize('Bot closed.', (fg(19), bg(45))))

    db = pickledb.load('./files/data.json', False) # this was the only way i could make cross-cog variables work
    t0 = t0
    version = botvernum

    # make the config available on the bot object incase we need cfg stuff in cogs, doing it this way saves us some IO time re-reading the config in each cog
    cfg = {
    # 'token':token, # omitted for safety reasons, only this file needs the bot token
    'defaultprefix': cfg['defaultprefix']
    }
bot = Bot(command_prefix=get_prefix, status=discord.Status.idle, activity=discord.Game(name=f"Loading... please wait! | {botname} {botvernum}"), description="Delta 1 is a utility Discord bot that is primarily used in mutual servers of it's owner.", intents=discord.Intents.all(), case_insensitive=True)

# ------ Var Definitions ------



# ------ Func Definitions ------

def ensure_logfile():
    if not os.path.exists('logs/bot.log'):
        if not os.path.exists('logs'):
            # create logs dir if not exist
            os.mkdir('logs')
        # initialize log file
        with open("logs/bot.log", "w") as f:
            f.write('')
ensure_logfile()

# ------ Func Definitions ------




# ------ Events ------
####################################
## MOVED TO files/cogs/events.py ##
####################################
# ------ Events ------



# ------ Listeners ------
####################################
## MOVED TO files/cogs/default.py ##
####################################
# ------ Listeners ------



# ------ Commands ------
####################################
## MOVED TO files/cogs/default.py ##
####################################
# ------ Commands ------



loaded = []
extensions = {
    'files.cogs.default',
    'files.cogs.events',
    'files.cogs.interactions',
    'files.cogs.error_handler2',
    'files.cogs.admin',
    'files.cogs.fun'
}

async def load_cogs():
    for extension in extensions:
        try:
            await bot.load_extension(extension)
        except Exception as e:
            print(stylize(f'There was an error while loading extension "{extension}"   -   Error: {e}', fg(1)))
        else:
            loaded.append(extension)

if __name__ == '__main__':
    bot.run(token)
