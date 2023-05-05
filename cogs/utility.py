import discord
from discord import slash_command
from discord.ext import commands


class Utility(commands.Cog, name="utility"):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(brief="Information about the server")
    async def serverinfo(self, ctx: discord.ApplicationContext):
        guild = ctx.guild
        owner = await guild.fetch_member(guild.owner_id)
        features = ""
        embed = discord.Embed(color=discord.Color.random(), title=guild.name)
        embed.description = f"""
**Owner:** {owner.mention}
**Members:** {guild.member_count}
**Roles:** {len(await guild.fetch_roles())}
**Verification:** {str(guild.verification_level).title()}
**Channels:** {len(guild.text_channels)} Text, {len(guild.voice_channels)} Voice
**Created:** <t:{round(guild.created_at.timestamp())}:R>
**Emojis:** {len(guild.emojis)}
**Stickers:** {len(guild.stickers)}
        """
        embed.set_thumbnail(url=guild.icon.url)
        embed.set_footer(text=f"ID: {guild.id}")
        if (guild.banner):
            embed.set_image(url=guild.banner.url)
        for feature in guild.features:
            features += f"{feature}, "
        features = features[:-2].replace("_", " ").title()  # Cut off trailing ", " fix casing and remove underscores
        embed.add_field(name="Features", value=features)
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Utility(bot))
