import discord
from discord import slash_command
from discord.ext import commands
from discord.commands import SlashCommandGroup
import utils
from utils import *


class Currency(commands.Cog, name="currency"):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(brief="Check your balance")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def balance(self, ctx):
        """ Check your balance """
        cursor = await utils.mysql_login()
        database = cursor.cursor()
        database.execute("SELECT cash, bank FROM economy WHERE UID = %s", [ctx.author.id])
        result = database.fetchall()
        database.close()

        embed = discord.Embed(colour=utils.Colors.blue)

        if not result:
            result = [(0, 0)]
            embed.add_field(name="WARNING",
                            value="***Please make sure you agree to our [privacy policy](https://github.com/MiataBoy) before continuing.***\nThis warning will disappear when you earn money.")

        embed.description = f"You have {utils.Emotes.cash} `{f'{result[0][0]:_}'.replace('_', '.')}` in your wallet\nYou have {utils.Emotes.bankCard} `{f'{result[0][1]:_}'.replace('_', '.')}` in your bank"

        return await ctx.respond(embed=embed, ephemeral=True)

    settings = SlashCommandGroup("settings", "view your settings")

    @settings.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def overview(self, ctx):
        try:
            cursor = await utils.mysql_login()
            database = cursor.cursor()
            database.execute("SELECT config FROM settings WHERE GUILD = %s", [ctx.guild.id])
            result = database.fetchall()
            database.close()

            return await ctx.respond(result)
        except Exception as e:
            return await ctx.respond(e)

    @settings.command()

    @commands.cooldown(1, 5, commands.BucketType.user)
    async def currency(self, ctx, status: discord.SlashCommandOptionType.boolean):
        await ctx.respond(status)

def setup(bot):
    bot.add_cog(Currency(bot))
