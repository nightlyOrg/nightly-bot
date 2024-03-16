import discord
import json
from discord import Intents, Status, Activity, ActivityType
from serviceProviders.migrationProvider import run_migrations

from config.vault import token
from config.app import Settings
from serviceProviders.seedProvider import run_seeders
from utilities.database import mysql_login, selector, modifyData
from datetime import datetime

is_seeding_enabled = Settings().get_setting("seeding")

intents = Intents(guilds=True)
bot = discord.Bot(intents=intents, status=Status.dnd,
                  activity=Activity(type=ActivityType.watching, name="you"))

bot.load_extensions("cogs")  # Loads all cogs in the cogs folder
bot.load_extensions("cogs.events")


@bot.listen()
async def on_connect():
    await run_migrations()
    if is_seeding_enabled: await run_seeders()
    print('-' * 50)
    print('✓ Migrations finished successfully.')
    print(f'✓ {bot.user} is connected to Discord.')


@bot.listen()
async def on_ready():
    # await bot.sync_commands() #You might need to uncomment this if the slash commands aren't appearing
    print('-' * 50)
    print(f'✓ Logged in as {bot.user} successfully.')


@bot.check
async def guild_only(ctx):
    return ctx.guild is not None


@bot.check
async def block_disabled_commands(ctx):
    result = (await selector("SELECT config FROM settings WHERE guild_id = %s", [ctx.guild.id]))
    if result == ():
        configuration = {'currency': True, 'socials': True}
        configuration = json.dumps(configuration)
        await modifyData("INSERT INTO settings (guild_id, config) VALUES (%s, %s)", [ctx.guild.id, configuration])
        print(f"{datetime.now().__format__('%a %d %b %y, %H:%M:%S')} - Corrected guild absence in settings upon command execution.")
    result = (await selector("SELECT config FROM settings WHERE guild_id = %s", [ctx.guild.id]))[0]
    result = json.loads(result)

    cog = ctx.cog.__class__.__name__

    if cog.lower() not in result:
        return True
    elif cog.lower() in result and result[cog.lower()]:
        return True
    else:
        return False


bot.run(token)
