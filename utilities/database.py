from config import database
import mysql.connector as mysql


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
    print(result)
    return result


async def saveData(query: str, variables: list) -> None:
    cursor = await mysql_login()
    db = cursor.cursor()
    db.execute(query, variables)
    cursor.commit()
    db.close()
    cursor.close()
