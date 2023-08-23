import discord
import json
from discord import Intents, Status, Activity, ActivityType

from config import token
from utilities.database import mysql_login, selector, modifyData
from datetime import datetime
intents = Intents(guilds=True)
bot = discord.Bot(intents=intents, status=Status.dnd,
                  activity=Activity(type=ActivityType.watching, name="you"))

bot.load_extensions("cogs")  # Loads all cogs in the cogs folder
bot.load_extensions("cogs.events")
print(bot.extensions)
BOOTED = False


@bot.listen()
async def on_connect():
    print('Connected to Discord!')
    print('Connecting to database')
    cursor = await mysql_login()
    database = cursor.cursor()
    print('Connected to database\nCreating the required tables if necessary')
    database.execute("CREATE TABLE IF NOT EXISTS settings (GUILD VARCHAR(20) PRIMARY KEY, config JSON)")
    database.execute("CREATE TABLE IF NOT EXISTS economy (UID VARCHAR(20) PRIMARY KEY, CASH FLOAT SIGNED, BANK FLOAT SIGNED)")
    database.execute("CREATE TABLE IF NOT EXISTS cooldowns (UID VARCHAR(20) PRIMARY KEY, command VARCHAR(20), cooldown INT)")
    print('Tables have been created')
    database.close()


@bot.listen()
async def on_ready():
    global BOOTED
    if BOOTED:
        print("Reconnect(?)")
    if not BOOTED:
        # await bot.sync_commands() #You might need to uncomment this if the slash commands aren't appearing
        print(f'Logged in as {bot.user}')
        print('------')
        BOOTED = True


@bot.check
async def guild_only(ctx):
    return ctx.guild is not None


@bot.check
async def block_disabled_commands(ctx):
    result = (await selector("SELECT config FROM settings WHERE GUILD = %s", [ctx.guild.id]))
    if result == ():
        configuration = {'currency': True, 'socials': True}
        configuration = json.dumps(configuration)
        await modifyData("INSERT INTO settings (GUILD, config) VALUES (%s, %s)", [ctx.guild.id, configuration])
        print(f"{datetime.now().__format__('%a %d %b %y, %H:%M:%S')} - Corrected guild absence in settings upon command execution.")
    result = (await selector("SELECT config FROM settings WHERE GUILD = %s", [ctx.guild.id]))[0]
    result = json.loads(result)

    cog = ctx.cog.__class__.__name__

    if cog.lower() not in result:
        return True
    elif cog.lower() in result and result[cog.lower()]:
        return True
    else:
        return False

bot.run(token)
