import discord
import random
from discord import slash_command, option
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

        embed.description = f"You have {Emotes.cash} `{f'{round(result[0], 2):_}'.replace('_', '.')}` in your wallet\nYou have {Emotes.bankCard} `{f'{round(result[1], 2):_}'.replace('_', '.')}` in your bank"

        return await ctx.respond(embed=embed, ephemeral=True)

    @slash_command(brief="Check your balance")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def daily(self, ctx):
        cooldownStatus = await checkCooldown(ctx)
        if cooldownStatus is not True:
            return await ctx.respond(f'Sorry, but you still have to wait till <t:{cooldownStatus}:f>')
        await createCooldown(ctx, 24)
        dailyAmount = random.randint(300, 500)
        await modifyData("INSERT INTO economy (UID,CASH, BANK) VALUES(%s, %s, %s) ON DUPLICATE KEY UPDATE CASH = CASH + %s", [ctx.author.id, dailyAmount, 0, dailyAmount])
        return await ctx.respond(f'Congratulations! You got {dailyAmount:.2f}.')

    @slash_command()
    @option("amount", int, description="The amount to deposit onto your bank", required=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def deposit(self, ctx, amount):
        """ Deposit money onto your bank """
        cash_balance = (await selector('SELECT cash FROM economy WHERE UID = %s', [ctx.author.id]))[0]
        print(cash_balance)
        if amount > cash_balance:
            return await ctx.respond(f"You only have {cash_balance:.2f}. You are {(amount-cash_balance):.2f} too short.")

        await modifyData('UPDATE economy SET cash = cash - %s, bank = bank + %s WHERE UID = %s', [amount, amount, ctx.author.id])

        return await ctx.respond(f"You have deposited {amount:.2f} cash into your bank account!")


def setup(bot):
    bot.add_cog(Currency(bot))
