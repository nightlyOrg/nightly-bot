from discord.commands import SlashCommandGroup
from discord.ext import commands
import utils
import json
import discord


class Settings(commands.Cog, name="settings"):
    def __init__(self, bot):
        self.bot = bot

    settings = SlashCommandGroup("settings", "view your settings")

    @settings.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def overview(self, ctx):
        """ View your server's settings """
        cursor = await utils.mysql_login()
        database = cursor.cursor()
        database.execute("SELECT config FROM settings WHERE GUILD = %s", [ctx.guild.id])
        result = database.fetchall()[0][0]
        database.close()

        result = json.loads(result)
        overview = ""
        for setting in result:
            overview += f"**{setting}:** {'Enabled' if result[setting] else 'Disabled'}\n"

        embed = discord.Embed()
        embed.title = f"Settings for {ctx.guild.name}"
        embed.description = overview
        embed.colour = utils.Colors.green

        return await ctx.respond(embed=embed)

    @settings.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def currency(self, ctx, enabled: discord.SlashCommandOptionType.boolean):
        """ Disable or enable currency """
        cursor = await utils.mysql_login()
        database = cursor.cursor()
        database.execute("SELECT config FROM settings WHERE GUILD = %s", [ctx.guild.id])
        result = database.fetchall()[0][0]
        result = json.loads(result)
        result['currency'] = enabled
        newConfig = json.dumps(result)

        database.execute("UPDATE settings SET config = %s WHERE GUILD = %s", [newConfig, ctx.guild.id])
        cursor.commit()
        database.close()
        cursor.close()
        return await ctx.respond(f"Currency is now {'enabled' if result['currency'] else 'disabled'}.")


def setup(bot):
    bot.add_cog(Settings(bot))
