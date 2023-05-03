# Nightly bot
Nightly is an open-source discord bot for any server, providing the best of the features that it offers. Nightly is a public version of [Paw](https://github.com/MiataBoy/Paw), the bot powering [The Paw Kingdom](https://discord.gg/tpk).

## Features
🤗 Social interaction commands (hug, kiss, boop...)

💸 Global currency commands

⚙ Configurable settings to disable/enable parts of our bot

## Selfhosting
Nightly is self-hosted with ease, as it was made to be minimal and compact.

1. Create a bot account on https://discord.com/developers/applications
2. Invite the bot with oauth scopes `bot` and `application.commands` to a guild of choice
3. clone this repository onto a server (If you don't have one, you may find VPS's for cheap at https://ovh.com) with `git clone https://github.com/NightlyOrg/nightly-bot.git`
4. Make sure Python 3.11+ is installed
5. Run `pip install -r requirements.txt`
6. Use PM2 or a similar tool to run the bot (`pm2 start bot.py --name Nightly --interpreter python3`)

#### ⚠ **We will not provide further support with self-hosting.** ⚠
