import random
import discord
from discord import option, slash_command
from discord.ext import commands
import utilities.jobs as jobs
from utilities.data import Colors, Emotes
from utilities.database import (checkCooldown, createCooldown, modifyData,
                                selector)


class Currency(commands.Cog, name="currency"):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(brief="Check your balance")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def balance(self, ctx):
        """ Check your balance """
        embed = discord.Embed(colour=Colors.blue)

        result = await selector("SELECT cash, bank FROM economy WHERE UID = %s", [ctx.author.id])

        embed.description = f"You have {Emotes.cash} `{f'{round(result[0], 2):_}'.replace('_', '.')}` in your wallet\nYou have {Emotes.bankCard} `{f'{round(result[1], 2):_}'.replace('_', '.')}` in your bank"

        return await ctx.respond(embed=embed, ephemeral=True)

    @slash_command(brief="Check your balance")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def daily(self, ctx):
        cooldown_status = await checkCooldown(ctx)
        if cooldown_status is not True:
            return await ctx.respond(f'Sorry, but you still have to wait till <t:{cooldown_status}:f>', ephemeral=True)
        await createCooldown(ctx, 24)
        daily_amount = random.uniform(300, 500)
        await modifyData("INSERT INTO economy (UID,CASH, BANK) VALUES(%s, %s, %s) ON DUPLICATE KEY UPDATE CASH = CASH + %s", [ctx.author.id, daily_amount, 0, daily_amount])
        return await ctx.respond(f'Congratulations! You got {daily_amount:.2f}.', ephemeral=True)

    @slash_command()
    @option("amount", int, description="The amount to deposit onto your bank", required=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def deposit(self, ctx, amount):
        """ Deposit money onto your bank """
        cash_balance = (await selector('SELECT CASH FROM economy WHERE UID = %s', [ctx.author.id]))[0]
        print(cash_balance)
        if amount > cash_balance:
            return await ctx.respond(f"You only have {cash_balance:.2f}. You are {(amount-cash_balance):.2f} too short.", ephemeral=True)

        await modifyData('UPDATE economy SET CASH = CASH - %s, BANK = BANK + %s WHERE UID = %s', [amount, amount, ctx.author.id])

        return await ctx.respond(f"You have deposited {amount:.2f} cash into your bank account!", ephemeral=True)

    @slash_command()
    @option("amount", int, description="The amount to withdraw from your bank", required=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def withdraw(self, ctx, amount):
        """ Withdraw money from your bank """
        cash_balance = (await selector('SELECT BANK FROM economy WHERE UID = %s', [ctx.author.id]))[0]
        print(cash_balance)
        if amount > cash_balance:
            return await ctx.respond(f"You only have {cash_balance:.2f}. You are {(amount-cash_balance):.2f} too short.", ephemeral=True)

        await modifyData('UPDATE economy SET BANK = BANK - %s, CASH = CASH + %s WHERE UID = %s', [amount, amount, ctx.author.id])

        return await ctx.respond(f"You have withdrawn {amount:.2f} cash from your bank account!", ephemeral=True)

    @slash_command()
    @option("job", str, description="The job you want to work", required=True, autocomplete=jobs.Job.autocomplete)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def work(self, ctx, job):
        """ Work a job """
        if job.title() not in jobs.Job.joblist:
            return await ctx.respond("Please select a valid job!", ephemeral=True)
        work = jobs.Job(job)
        if random.randint(0, 100) > work.success_chance:  # If job FAILS
            return await ctx.respond(f"{Emotes.crossmark} {work.fail_message}")
        pay = random.randint(work.min_pay, work.max_pay)
        await modifyData("INSERT INTO economy (UID, CASH, BANK) VALUES(%s, %s, 0) ON DUPLICATE KEY UPDATE CASH = CASH + %s", [ctx.author.id, pay, pay])
        return await ctx.respond(f"{Emotes.checkmark} You did your job well!\nPay: {pay} {Emotes.cash}")

    @slash_command()
    @option("user", discord.User, description="The person that receives the payment")
    @option("amount", int, description="The amount of money you want to pay", min_value=1)
    async def pay(self, ctx, user, amount):
        if ctx.author == user:
            return await ctx.respond("You already own the money you are attempting to pay yourself...", ephemeral=True)
        if (await selector('SELECT CASH FROM economy WHERE UID = %s', [ctx.author.id])) < amount:
            return await ctx.respond(f"You do not have {amount} in cash.", ephemeral=True)
        await modifyData("INSERT INTO economy (UID, CASH, BANK) VALUES(%s, %s, 0) ON DUPLICATE KEY UPDATE CASH = CASH + %s", [user.id, amount, amount])


def setup(bot):
    bot.add_cog(Currency(bot))
