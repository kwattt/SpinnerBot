import asyncio
from discord import Intents
from discord.ext import commands
from os import getenv

def sv_prefix(client, msg):
    return getenv('DISCORD_PREFIX')

cogs = [
    "modules.roles",
    "modules.errors",
    "modules.purge",
    "modules.mentions"
]

intents = Intents.default()
intents.message_content = True

client = commands.Bot(bot=True, reconnect=True, command_prefix=sv_prefix,
                    description="Interlinked v0.2b", intents=intents)

async def main():
    if __name__ == "__main__":
        for cog in cogs:
            try:
                await client.load_extension(cog)
                print("{} loaded without any problems.".format(cog))

            except Exception as e:
                print("Error loading cog %s" % cog)
                print("{}: {}".format(type(e).__name__, e))

asyncio.run(main())

client.run(getenv('DISCORD_TOKEN'))