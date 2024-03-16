from serviceProviders.migrationProvider import kill_active_migrations, run_migrations
from serviceProviders.seedProvider import run_seeders
from discord import option, SlashCommandGroup
from discord.ext import commands


class DevOps(commands.Cog, name="dev_ops"):
    def __init__(self, bot):
        self.bot = bot

    dev_ops = SlashCommandGroup("dev_ops", "Developer operations")

    @dev_ops.command()
    @commands.is_owner()
    @option("fresh", bool, description="Whether to delete all tables and then migrate.")
    async def migrate(self, ctx, fresh: bool = False):
        """ Migrate the database """
        if fresh:
            await kill_active_migrations()
            message = await ctx.respond("Killed active migrations...", ephemeral=True)

        await run_migrations()
        await ctx.respond("✓ Migrations finished successfully.", ephemeral=True)

    @dev_ops.command()
    @commands.is_owner()
    async def seed(self, ctx):
        """ Seed the database """
        await run_seeders()
        await ctx.respond("✓ Seeders finished successfully.", ephemeral=True)

def setup(bot):
    bot.add_cog(DevOps(bot))
