import random
import discord
import aiohttp
import config
import mysql.connector as mysql

class Colors:
    blue = 0xadd8e6
    red = 0xf04747
    green = 0x90ee90
    orange = 0xfaa61a

class Emotes:
    bankCard = '<a:MoneyCard2:1103307033941385247>'
    cash = '<:cash:1103307142410272768>'

async def interactions(ctx, members, name, error_name, giflist, altname=None):
    if isinstance(giflist, str):
        json = await apireq(giflist)
        image = json['link']
    else:
        image = random.choice(giflist)
    display_giflist = []
    for x in members:
        display_giflist.append(x.display_name)
    if len(members) >= 3:
        display_giflist.append(f"and {display_giflist.pop(-1)}")
    if len(members) == 2:
        display_giflist = f"{display_giflist[0]} and {display_giflist[1]}"
    else:
        display_giflist = ', '.join(display_giflist)
    embed = discord.Embed(
        description=f"**{ctx.author.display_name}** {name} **" + display_giflist + "**",
        color=discord.Color.blue())
    embed.set_thumbnail(url=image)
    view = interactionsView(ctx, members, name, error_name, giflist, altname)
    await ctx.respond(embed=embed, view=view)


class interactionsView(discord.ui.View):
    def __init__(self, ctx, members, name, error_name, giflist, altname=None):
        super().__init__(timeout=600)
        self.ctx = ctx
        self.members = members
        self.name = name
        self.error_name = error_name
        self.giflist = giflist
        self.altname = altname
        if self.altname is None:
            self.button_callback.label = f"{self.error_name.title()} back!"
        else:
            self.button_callback.label = f"{self.altname} back!"

    @discord.ui.button()
    async def button_callback(self, button, interaction):
        if interaction.user not in self.members:
            return await interaction.response.send_message(f"You weren't {self.name}!", ephemeral=True)
        self.members.remove(interaction.user)
        if len(self.members) == 0:
            self.disable_all_items()
            await interaction.message.edit(view=self)
        if isinstance(self.giflist, str):
            json = await apireq(self.giflist)
            image = json['link']
        else:
            image = random.choice(self.giflist)
        embed = discord.Embed(
            description=f"**{interaction.user.name}** {self.name} **" + self.ctx.author.name + "** back!",
            color=discord.Color.blue())
        embed.set_thumbnail(url=image)
        await interaction.response.send_message(embed=embed)


async def mentionconverter(self, ctx, members):
    memberlist = []
    guild = self.bot.get_guild(ctx.guild.id)
    members = discord.utils.raw_mentions(members)
    for member in members:
        member = await guild.fetch_member(member)
        memberlist.append(member)
    return memberlist


async def feelings(ctx, members, name, giflist):
    embed = discord.Embed(color=discord.Color.blue())
    embed.set_thumbnail(url=random.choice(giflist))
    if members is None:
        embed.description = f"**{ctx.author.display_name}** {name}!"
    else:
        display_giflist = []
        for x in members:
            display_giflist.append(x.display_name)
        if len(members) >= 3:
            display_giflist.append(f"**and **{display_giflist.pop(-1)}")
        if len(members) == 2:
            display_giflist = f"{display_giflist[0]}** and **{display_giflist[1]}"
        else:
            display_giflist = ', '.join(display_giflist)
        embed.description = f"**{ctx.author.display_name}** {name} because of **{display_giflist}**"
    await ctx.respond(embed=embed)


async def apireq(url):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(url) as r:
            js = await r.json()
            return js

async def mysql_login():
    return mysql.connect(
        host=config.database['host'],
        user=config.database['user'],
        password=config.database['password'],
        database=config.database['database'])