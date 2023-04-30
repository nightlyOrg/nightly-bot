import data
from discord.ext import commands
from discord import slash_command, option, Option
from utils import *
import aiohttp


class socials(commands.Cog, name="social"):
    def __init__(self, bot):
        self.bot = bot
        self.help_icon = "♥️"

    @slash_command(brief="Snuggle someone")
    @option("members", str, description="Mention users to snuggle")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def snuggle(self, ctx, members: str):
        """ Snuggle the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "snuggled", 'snuggle', data.snuggle)

    @slash_command(brief="Hug someone")
    @option("members", str, description="Mention users to hug")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hug(self, ctx, *, members: str):
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "hugged", 'hug', data.hug, 'Hug')

    @slash_command(brief="Boop someone")
    @option("members", str, description="Mention users to boop")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def boop(self, ctx, *, members: str):
        """ Boop the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "booped", 'boop', data.boop)

    @slash_command(brief="Kiss someone")
    @option("members", str, description="Mention users to kiss")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def smooch(self, ctx, *, members: str):
        """ Smooch the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "smooched", 'smooch', data.smooch)

    @slash_command(brief="Lick someone")
    @option("members", str, description="Mention users to lick")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lick(self, ctx, *, members: str):
        """ Lick the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "licked", 'lick', data.lick)

    @slash_command(brief="Give someone bellyrubs")
    @option("members", str, description="Mention users to bellrub")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bellyrub(self, ctx, *, members: str):
        """ Give bellyrubs to the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "bellyrubbed", 'rub the belly of', data.bellyrub, "Rub")

    @slash_command(brief="Nuzzle someone")
    @option("members", str, description="Mention users to nuzzle")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nuzzle(self, ctx, *, members: str):
        """ Nuzzle the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "nuzzled", 'nuzzles', data.nuzzle)

    @slash_command(brief="Cuddle someone")
    @option("members", str, description="Mention users to cuddle")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cuddle(self, ctx, *, members: str):
        """ Cuddle the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "cuddled", 'cuddle', data.cuddle)

    @slash_command(brief="Feed someone")
    @option("members", str, description="Mention users to feed")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def feed(self, ctx, *, members: str):
        """ Feed the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "fed", 'feed', data.feed)

    @slash_command(brief="Glomp someone")
    @option("members", str, description="Mention users to glomp")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def glomp(self, ctx, *, members: str):
        """ Glomp on the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "glomped", 'glomp', data.glomp)

    @slash_command(brief="Highfive someone")
    @option("members", str, description="Mention users to highfive")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def highfive(self, ctx, *, members: str):
        """ Highfive the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "highfived", 'highfive', data.highfive)

    @slash_command(brief="Rawr")
    @option("members", str, description="Mention users to rawr at")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rawr(self, ctx, *, members: str):
        """ Rawr at the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "rawred at", 'rawr at', data.rawr, "Rawr")

    @slash_command(brief="Howl to the moon, or someone")
    @option("members", str, description="Mention users to howl at")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def howl(self, ctx, *, members: str):
        """ Howl at the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "howled at", 'howl at', data.awoo, "Howl")

    @slash_command(brief="Pat someone")
    @option("members", str, description="Mention users to pat")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pat(self, ctx, *, members: str):
        """ Pat the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "pats", 'pat', data.pet, 'Pat')

    @slash_command(brief="Give a cookie to someone")
    @option("members", str, description="Mention users to give a cookie to")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cookie(self, ctx, *, members: str):
        """ Give cookies to the specified people """
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "gave a cookie to", 'give a cookie to', data.cookie, "Give a cookie")

    @slash_command(brief="Dance with someone")
    @option("members", str, description="Mention users to dance with", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dance(self, ctx, *, members: str = None):
        """ Dance with someone """
        if not members:
            memberlist = None
            return await feelings(ctx, memberlist, "dances", data.dance)
        memberlist = await mentionconverter(self, ctx, members)
        await interactions(ctx, memberlist, "danced with", "dance with", data.dance, "Dance")

    @slash_command(brief="Blush")
    @option("members", str, description="Mention users that made you blush", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def blush(self, ctx, *, members: str = None):
        """ Blush (optionally because of specified people) """
        if not members:
            memberlist = None
        else:
            memberlist = await mentionconverter(self, ctx, members)
        await feelings(ctx, memberlist, "blushes", data.blush)

    @slash_command(brief="Be happy")
    @option("members", str, description="Mention users that made you happy", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def happy(self, ctx, *, members: str = None):
        """ Be happy (optionally because of specified people) """
        if not members:
            memberlist = None
        else:
            memberlist = await mentionconverter(self, ctx, members)
        await feelings(ctx, memberlist, "smiles", data.happy)

    @slash_command(brief="Wag your tail ")
    @option("members", str, description="Mention users that made you wag", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wag(self, ctx, *, members: str = None):
        """ Wag your tail (Optionally because of specified people) """
        if not members:
            memberlist = None
        else:
            memberlist = await mentionconverter(self, ctx, members)
        await feelings(ctx, memberlist, "wags their tail", data.wag)

    @slash_command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fact(self, ctx):
        """ Get a random animal fact """
        facts = random.choice(["https://some-random-api.ml/facts/dog", "https://some-random-api.ml/facts/cat", "https://some-random-api.ml/facts/panda",
                               "https://some-random-api.ml/facts/fox", "https://some-random-api.ml/facts/bird", "https://some-random-api.ml/facts/koala"])

        async with aiohttp.ClientSession() as cs:
            async with cs.get(facts) as r:
                js = await r.json()

                await ctx.respond(js['fact'])

    @slash_command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fox(self, ctx):
        """ Get a random fox """
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://randomfox.ca/floof/") as r:
                js = await r.json()

                e = discord.Embed(title="Floofy fox!", color=discord.Color.orange())
                e.set_image(url=js['image'])
                await ctx.respond(embed=e)

    @slash_command(brief="Give someone's avatar a rainbow overlay")
    @option("user", discord.Member, description="Select a user")
    @option("border", bool, description="Make it a border?", required=False)
    @option("server-avatar", bool, description="Use their server avatar?", required=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gay(self, ctx, user: discord.Member = None, border: bool = False, server_avatar: bool = False):
        """ Gay overlay on avatar """
        link = ""
        if not user:
            if ctx.message:  # additional check to make slash commands not break at .message.reference
                if ctx.message.reference:
                    reference = await ctx.fetch_message(ctx.message.reference.message_id)
                    user = reference.author
            else:
                user = ctx.author
        if not server_avatar:
            url = user.avatar.url
        else:
            url = user.display_avatar.url
        if not border:
            link = f"https://some-random-api.ml/canvas/gay/?avatar={url}"
        else:
            link = f"https://some-random-api.ml/canvas/misc/lgbt/?avatar={url}"
        e = discord.Embed(color=discord.Color.random())
        e.set_image(url=link)
        e.set_footer(text=f"Gay avatar: {user}")
        await ctx.respond(embed=e)


def setup(bot):
    bot.add_cog(socials(bot))
