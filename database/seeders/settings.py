"""
Seeders are responsible for filling the database schemas.
The bot will run these upon start-up if enabled in config/app.py.

The bot provides seeding commands to run these Seeders manually,
but it is not recommended to use these commands unless you know what
you are doing.

If you are self-hosting this bot for public use, we recommend you
establish a privacy policy, and refrain from touching these commands
while in production. The Nightly organization and Nightem Software
Foundation are not responsible for any data loss or corruption as
a result of using these commands in any wrong or untimely manner.
"""
import json


class Seeder:
    table = "settings"
    columns = [
        {"guild_id": "1102269821170749573"},
        {"config": json.dumps({'currency': True, 'socials': True})},
    ]

    def getTable(self):
        return self.table

    def getColumns(self):
        return self.columns