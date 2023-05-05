import json
import random
import aiohttp
import discord
import mysql.connector as mysql
import config


class Colors:
    blue = 0xadd8e6
    red = 0xf04747
    green = 0x90ee90
    orange = 0xfaa61a


class Emotes:
    bankCard = '<a:MoneyCard2:1103307033941385247>'
    cash = '<:cash:1103307142410272768>'


async def checkSettingsValue(ctx, setting: str):
    cursor = await mysql_login()
    database = cursor.cursor()
    database.execute("SELECT config FROM settings WHERE GUILD = %s", [ctx.guild.id])
    result = database.fetchall()[0][0]
    result = json.loads(result)

    if not result[setting]:
        return await ctx.respond(f'{setting} is disabled here.', ephemeral=True)
    else:
        return

async def mysql_login():
    return mysql.connect(
        host=config.database['host'],
        user=config.database['user'],
        password=config.database['password'],
        database=config.database['database'])
