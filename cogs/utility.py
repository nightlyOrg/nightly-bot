import discord
from discord import slash_command
from discord.ext import commands
from utilities.data import Colors


class Utility(commands.Cog, name="utility"):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(brief="Information about the server")
    async def serverinfo(self, ctx: discord.ApplicationContext):
        guild = ctx.guild
        owner = await guild.fetch_member(guild.owner_id)
        embed = discord.Embed(color=Colors.blue, title=guild.name)
        embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Roles", value=len(await guild.fetch_roles()), inline=True)
        embed.add_field(name="Owner", value=owner.mention)
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Utility(bot))
