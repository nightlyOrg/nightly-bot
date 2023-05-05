import discord
from discord.ext import commands
from utilities.data import Emotes, Colors


# from cogs.admin import admin_only

class error(commands.Cog, name="Error"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, err):
        if isinstance(err, commands.CommandNotFound):
            return

        if isinstance(err, commands.MissingPermissions):
            perms = "`" + '`, `'.join(err.missing_permissions) + "`"
            return await ctx.respond(f"{Emotes.crossmark} **You are missing {perms} permissions.**", ephemeral=True)

        if isinstance(err, commands.BotMissingPermissions):
            perms = "`" + '`, `'.join(err.missing_permissions) + "`"
            return await ctx.respond(f"{Emotes.crossmark} **I'm missing {perms} permissions**", ephemeral=True)

        if isinstance(err, commands.CommandOnCooldown):
            return await ctx.respond(f"{Emotes.crossmark} **This command is on cooldown for {round(err.retry_after)} more seconds.**", ephemeral=True)

        if isinstance(err, commands.MemberNotFound):
            return await ctx.respond(f"{Emotes.confused} **Could not find user `{err.argument}`", ephemeral=True)

        if isinstance(err, discord.NotFound):
            return await ctx.respond(f"{Emotes.confused} I could not find the argument you have provided.", ephemeral=True)


def setup(bot):
    bot.add_cog(error(bot))
