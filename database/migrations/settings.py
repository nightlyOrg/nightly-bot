"""
Migrations are responsible for generating the database schemas.
The bot will run these upon start-up, if the tables do not exist.

Existing tables will not be modified or duplicated. If you wish
for these to be modified, you will need to manually run the
migrations or modify the database manually.

The bot provides migration commands to run these migrations manually,
but it is not recommended to use these commands unless you know what
you are doing. These commands accept a fresh migration, and existent
migration. Implying that a fresh migration will delete all existing
schemas and create new ones. Existent migrations will only create
schemas that do not exist, and will not modify existing ones.

If you are self-hosting this bot for public use, we recommend you
establish a privacy policy, and refrain from touching these commands
while in production. The Nightly organization and Nightem Software
Foundation are not responsible for any data loss or corruption as
a result of using these commands in any wrong or untimely manner.
"""


class Schema:
    name = "settings"
    columns = [
        "guild_id VARCHAR(20) PRIMARY KEY",
        "config LONGTEXT",
    ]

    def getName(self):
        return self.name

    def getColumns(self):
        return self.columns
