import aiohttp
import random
import discord


def memberlistAppend(members):
    memberlist = []
    for member in members:
        memberlist.append(member.display_name)
    if len(members) >= 3:
        memberlist.append(f"and {memberlist.pop(-1)}")
    if len(members) == 2:
        memberlist = f"{memberlist[0]} and {memberlist[1]}"
    else:
        memberlist = ', '.join(memberlist)
    return memberlist


async def interactions(ctx, members, action, giflist):
    if isinstance(giflist, str):
        json = await apireq(giflist)
        image = json['link']
    else:
        image = random.choice(giflist)
    memberlist = memberlistAppend(members)
    embed = discord.Embed(
        description=f"**{ctx.author.display_name}** {action} **" + memberlist + "**",
        color=discord.Color.blue())
    embed.set_thumbnail(url=image)
    return embed


class InteractionsView(discord.ui.View):
    def __init__(self, ctx, members, action, button_label, giflist, action_error=None):
        super().__init__(timeout=600)
        self.ctx = ctx
        self.members = members
        self.action = action
        self.giflist = giflist
        self.action_error = action_error
        self.button_callback.label = f"{button_label} back!"
        self.disable_on_timeout = True

    @discord.ui.button()
    async def button_callback(self, button, interaction):
        if interaction.user not in self.members:
            if not self.action_error:
                return await interaction.response.send_message(f"You weren't {self.action}!", ephemeral=True)
            else:
                return await interaction.response.send_message(f"You weren't {self.action_error}!", ephemeral=True)
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
            description=f"**{interaction.user.name}** {self.action} **" + self.ctx.author.name + "** back!",
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
        display_giflist = memberlistAppend(members)
        embed.description = f"**{ctx.author.display_name}** {name} because of **{display_giflist}**"
    await ctx.respond(embed=embed)


async def apireq(url):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(url) as r:
            js = await r.json()
            return js
