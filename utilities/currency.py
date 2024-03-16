from utilities.database import selector, modifyData


async def memberEntryInDatabase(memberId):
    """
    This function checks if a member is in the database economy table and if not, adds them to the table
    :param memberId: int
    :return: bool
    """
    if not await selector("SELECT * FROM economy WHERE user_id = %s", [memberId]):
        try:
            await modifyData("INSERT INTO economy (user_id, cash, bank) VALUES (%s, %s, %s)", [memberId, 0, 0])
        except Exception as error:
            print(f"Error in memberEntryInDatabase: {error}")
            return False

    return True
