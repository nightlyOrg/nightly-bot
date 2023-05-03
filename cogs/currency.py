from discord import slash_command
from discord.ext import commands
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
        result = database.fetchall()[0]
        database.close()

        embed = discord.Embed(colour=utils.Colors.blue)

        if not result:
            result = [(0, 0)]
            embed.add_field(name="WARNING",
                            value="***Please make sure you agree to our [privacy policy](https://github.com/MiataBoy) before continuing.***\nThis warning will disappear when you earn money.")

        embed.description = f"You have {utils.Emotes.cash} `{f'{result[0]:_}'.replace('_', '.')}` in your wallet\nYou have {utils.Emotes.bankCard} `{f'{result[1]:_}'.replace('_', '.')}` in your bank"

        return await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Currency(bot))
