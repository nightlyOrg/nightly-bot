import json
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from utilities.data import Colors
from utilities.database import modifyData, selector


class Settings(commands.Cog, name="settings"):
    def __init__(self, bot):
        self.bot = bot

    settings = SlashCommandGroup("settings", "view your settings")

    @settings.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def overview(self, ctx):
        """ View your server's settings """
        result = (await selector("SELECT config FROM settings WHERE GUILD = %s", [ctx.guild.id]))[0]

        result = json.loads(result)
        overview = ""
        for setting in result:
            overview += f"**{setting}:** {'Enabled' if result[setting] else 'Disabled'}\n"

        embed = discord.Embed()
        embed.title = f"Settings for {ctx.guild.name}"
        embed.description = overview
        embed.colour = Colors.green

        return await ctx.respond(embed=embed)

    @settings.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def currency(self, ctx, enabled: discord.SlashCommandOptionType.boolean):
        """ Disable or enable currency """
        result = (await selector("SELECT config FROM settings WHERE GUILD = %s", [ctx.guild.id]))[0]
        result = json.loads(result)
        result['currency'] = enabled
        new_config = json.dumps(result)

        await modifyData("UPDATE settings SET config = %s WHERE GUILD = %s", [new_config, ctx.guild.id])
        return await ctx.respond(f"Currency is now {'enabled' if result['currency'] else 'disabled'}.")

    @settings.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def socials(self, ctx, enabled: discord.SlashCommandOptionType.boolean):
        """ Disable or enable social interactions """
        result = (await selector("SELECT config FROM settings WHERE GUILD = %s", [ctx.guild.id]))[0]
        result = json.loads(result)
        result['socials'] = enabled
        new_config = json.dumps(result)

        await modifyData("UPDATE settings SET config = %s WHERE GUILD = %s", [new_config, ctx.guild.id])
        return await ctx.respond(f"Socials is now {'enabled' if result['socials'] else 'disabled'}.")


def setup(bot):
    bot.add_cog(Settings(bot))
