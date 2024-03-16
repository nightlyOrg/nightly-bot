"""
This file is used for generic configuration of the bot.
This includes changing debug mode, disabling or enabling
seeding, and other general settings for the bot.

It is recommended to change the ENVIRONMENT variable to
"production" when the bot is in production, and to set it
to "local" when the bot is in development. This will enable
or disable certain features of the bot, and will also
change the way the bot handles errors and other events.
"""


class Settings:
    environment = "local"
    debug = False
    seeding = True

    def get_setting(self, setting):
        return self.__getattribute__(setting)
