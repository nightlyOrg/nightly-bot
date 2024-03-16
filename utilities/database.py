from config.vault import database
import mysql.connector as mysql
import time


async def mysql_login():
    return mysql.connect(
        host=database['host'],
        user=database['user'],
        password=database['password'],
        database=database['database'])


async def selector(query: str, variables: list):
    cursor = await mysql_login()
    db = cursor.cursor()
    db.execute(query, variables)
    try:
        result = db.fetchall()[0]
    except IndexError:
        return ()
    db.close()
    cursor.close()
    return result


async def modifyData(query: str, variables: list) -> None:
    cursor = await mysql_login()
    db = cursor.cursor()
    db.execute(query, variables)
    cursor.commit()
    db.close()
    cursor.close()


async def createCooldown(ctx, hours: int):
    newTime = round(time.time()) + hours * 60 * 60
    await modifyData("INSERT INTO cooldowns (user_id, command, cooldown) VALUES (%s, %s, %s)", [ctx.author.id, ctx.command.name, newTime])


async def checkCooldown(ctx):
    currentTime = round(time.time())
    await mysql_login()
    cooldown = await selector("SELECT cooldown FROM cooldowns WHERE user_id = %s AND command = %s", [ctx.author.id, ctx.command.name])
    if not cooldown:
        return True
    elif cooldown:
        if currentTime > cooldown[0]:
            await modifyData("DELETE FROM cooldowns WHERE user_id = %s AND command = %s", [ctx.author.id, ctx.command.name])
            return True
        else:
            return cooldown[0]
