import discord
import random
from discord import slash_command
from discord.ext import commands
from utilities.database import selector, createCooldown, checkCooldown, modifyData
from utilities.data import Colors, Emotes


class Currency(commands.Cog, name="currency"):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(brief="Check your balance")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def balance(self, ctx):
        """ Check your balance """
        embed = discord.Embed(colour=Colors.blue)

        result = await selector("SELECT cash, bank FROM economy WHERE UID = %s", [ctx.author.id])

        if not result:
            result = (0, 0)
            embed.add_field(name="WARNING", value="***Please make sure you agree to our [privacy policy](https://github.com/MiataBoy) before continuing.***\nThis warning will disappear when you earn money.")

        embed.description = f"You have {Emotes.cash} `{f'{result[0]:_}'.replace('_', '.')}` in your wallet\nYou have {Emotes.bankCard} `{f'{result[1]:_}'.replace('_', '.')}` in your bank"

        return await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(Currency(bot))
