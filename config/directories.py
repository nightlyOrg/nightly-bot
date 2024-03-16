"""
Configuration file responsible for defining the directories
for the bot to use. Generally, it is not recommended to modify
these directories unless you know what you are doing. The bot
will not function properly if these directories are not defined
correctly.

If you change these directories, you will need to restart the
bot for the changes to take effect. Additionally, you should
ensure the directory locations are correct.
"""

import sys

if sys.platform == "win32":
    splitter = "\\"
else:
    splitter = "/"


class Directories:
    migrations = f"database{splitter}migrations"
    seeders = f"database{splitter}seeders"

    def get_directory(self, directory):
        return self.__getattribute__(directory)
