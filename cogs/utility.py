import json
import io
import zipfile
import aiohttp
import discord
import psutil
from discord import option, slash_command
from discord.ext import commands
from utilities.data import Colors, Links, gaslight


class Utility(commands.Cog, name="utility"):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def info(self, ctx):
        try:
            embed = discord.Embed()
            embed.colour = Colors.blue
            embed.description = f"""
{self.bot.user.name} is a bot developed by Nightly to service people with social interaction commands, currency commands and other utility commands. Nightly is an organization owned by MiataBoy & ToothyDev.

While {self.bot.user.name} is not yet complete, we are hard at work everyday to improve it, and add new features and commands. If you have suggestions, let us know through our discord or a github issue!

**Guilds:** {len(self.bot.guilds)}
**Users:** {sum(x.member_count for x in self.bot.guilds)}
**API Latency:** {round(self.bot.latency * 1000)}ms
**RAM:** {round((psutil.virtual_memory().used / 1000000000), 2)}GB used out of {round((psutil.virtual_memory().total / 1000000000), 2)}GB total ({psutil.virtual_memory().percent}% used)
**Disk:** {round((psutil.disk_usage('/').free / 1000000000), 2)}GB free out of {round((psutil.disk_usage('/').total / 1000000000), 2)}GB total ({(psutil.disk_usage('/').percent - 100) * (-1)}% free)

[[Invite]]({Links.invite}) [[Support]]({Links.discord}) [[Github]]({Links.github}) [[Privacy Policy]]({Links.privacy}) [[Terms of Service]]({Links.terms})
            """
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            return await ctx.respond(embed=embed)
        except Exception as e:
            return await ctx.respond(e)

    @slash_command(brief="Information about the server")
    async def serverinfo(self, ctx):
        """ Get the current server's info """
        guild = ctx.guild
        owner = await guild.fetch_member(guild.owner_id)
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
        if guild.banner:
            embed.set_image(url=guild.banner.url)
        features = ", ".join(guild.features).replace("_", " ").title()
        embed.add_field(name="Features", value=features)
        await ctx.respond(embed=embed)

    @slash_command(brief="Get all server stickers & emojis!")
    @discord.default_permissions(manage_guild=True)
    async def emoji_downloader(self, ctx):
        """ Download this server's emojis and stickers """
        saved_emojis = []
        saved_stickers = []
        total = len(ctx.guild.emojis) + len(ctx.guild.stickers)
        current = 0
        message = await ctx.respond(f"Downloading, this might take some time... (0 of {total})")
        zip_buffer = io.BytesIO()  # Create a BytesIO object to hold the ZIP file
        with zipfile.ZipFile(zip_buffer, 'w') as zipped_f:  # Create a ZIP file inside the buffer
            for emoji in ctx.guild.emojis:
                emoji_file_name = (emoji.name if emoji.name not in saved_emojis else emoji.name + str(saved_emojis.count(emoji.name) + 1)) + emoji.url[-4:]
                zipped_f.writestr(f"emojis/{emoji_file_name}", await emoji.read())
                saved_emojis.append(emoji.name)
                current += 1
                await message.edit_original_response(content=f"Downloading, this might take some time... ({current} of {total})")

            async with aiohttp.ClientSession() as session:
                for sticker in ctx.guild.stickers:
                    async with session.get(sticker.url) as response:
                        sticker_file_name = (sticker.name if sticker.name not in saved_stickers else sticker.name + str(saved_stickers.count(sticker.name) + 1)) + ".png"
                        zipped_f.writestr(f"stickers/{sticker_file_name}", await response.read())
                        saved_stickers.append(sticker.name)

        zip_buffer.seek(0)  # Reset the buffer position to the beginning so the next line reads the file from the start
        await message.edit_original_response(content="Here are all emojis and stickers of this guild!", file=discord.File(zip_buffer, filename="emojis_and_stickers.zip"))

    @slash_command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    @option("text", str, description="What do you want to tell / ask Nightly?")
    async def gpt(self, ctx, text):
        """ Talk to Nightly! """
        return await ctx.respond("This command is disabled indefinitely.", ephemeral=True)
        await ctx.defer()
        url = "GPT-API-URL-HERE"
        adata = {
            "model": "gpt-4",
            "messages": [{"role": "system", "content": f"""{gaslight} The user's name is {ctx.author.display_name}. Do not use the user's full name, use their call name derived from their full name."""},
                         {"role": "user", "content": text}],
            "max_tokens": 500
        }
        headers = {
            "Content-Type": "application/json"
        }
        retries = 0
        while retries < 4:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=json.dumps(adata)) as response:
                    if response.status == 200:
                        response_json = await response.json()
                        content = response_json["choices"][0]["message"]["content"]
                        return await ctx.respond(f"""**Prompt:** {text}\n**Paw:** {content}""")
                    else:
                        retries += 1
        await ctx.respond("Sorry, there has been an API error. Please try again")


def setup(bot):
    bot.add_cog(Utility(bot))
