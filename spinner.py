from discord.ext import commands
import json
from commons import loadFile

def sv_prefix(client, msg):
    prefix = loadFile("info.json")['prefix']
    return prefix

cogs = [
    "modules.roles",
    "modules.misc",
    "modules.errors"
    "modules.purge"
]

client = commands.Bot(bot=True, reconnect=True, command_prefix=sv_prefix,
                      description="Interlinked")

if __name__ == "__main__":
    for cog in cogs:
        try:
            client.load_extension(cog)
            print("{} loaded without any problems.".format(cog))

        except Exception as e:
            print("Error loading cog %s" % cog)
            print("{}: {}".format(type(e).__name__, e))

cfg = loadFile("data.json")
client.run(cfg["discord_key"])