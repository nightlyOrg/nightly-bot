import json
import traceback
from datetime import datetime
from discord.ext import commands
from utilities.database import mysql_login, selector, modifyData


# from cogs.admin import admin_only

class Logs(commands.Cog, name="Logs"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command(self, ctx):
        if ctx.guild:
            if (await selector("SELECT * FROM settings WHERE GUILD = %s", [ctx.guild.id])) == ():
                configuration = {'currency': True, 'socials': True}
                configuration = json.dumps(configuration)
                await modifyData("INSERT INTO settings (GUILD, config) VALUES (%s, %s)", [ctx.guild.id, configuration])
            print(f"{datetime.now().__format__('%a %d %b %y, %H:%M:%S')} - {ctx.guild.name} | {ctx.author} > {ctx.command}")
        else:
            print(f"{datetime.now().__format__('%a %d %b %y, %H:%M:%S')} - Direct Messages | {ctx.author} > {ctx.command}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"{datetime.now().__format__('%a %d %b %y, %H:%M:%S')} - Added to {guild.name}")
        print(f"{datetime.now().__format__('%a %d %b %y, %H:%M:%S')} - Loading default settings and inserting it into database")

        configuration = {'currency': True, 'socials': True}
        configuration = json.dumps(configuration)

        try:
            cursor = await mysql_login()
            database = cursor.cursor()
            database.execute("INSERT INTO settings (GUILD, config) VALUES (%s, %s)", [guild.id, configuration])
            cursor.commit()
            database.close()
            cursor.close()
        except Exception as error:
            print(f"{datetime.now().__format__('%a %d %b %y, %H:%M:%S')} - Received fatal connection | Could not complete operation")
            traceback.print_tb(error.__traceback__)

        else:
            print(f"{datetime.now().__format__('%a %d %b %y, %H:%M:%S')} - Successfully loaded and inserted default settings")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        print(f"{datetime.now().__format__('%a %d %b %y, %H:%M:%S')} - Removed from {guild.name}")
        print(f"{datetime.now().__format__('%a %d %b %y, %H:%M:%S')} - Deleting configuration settings from database...")

        try:
            cursor = await mysql_login()
            database = cursor.cursor()
            database.execute("DELETE FROM settings WHERE GUILD = %s", [guild.id])
            cursor.commit()
            database.close()
            cursor.close()
        except Exception as error:
            print(f"{datetime.now().__format__('%a %d %b %y, %H:%M:%S')} - Received fatal connection | Could not complete operation")
            traceback.print_tb(error.__traceback__)

        else:
            print(f"{datetime.now().__format__('%a %d %b %y, %H:%M:%S')} - Successfully deleted configuration settings from database")


def setup(bot):
    bot.add_cog(Logs(bot))
