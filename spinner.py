from discord.ext import commands
import json

def sv_prefix(client, msg):
    f_prefix = open("info.json", 'r', encoding="utf8")
    prefix = json.load(f_prefix)['prefix']
    f_cfg.close()
    return prefix

cogs = [
    "modules.roles"
]

client = commands.Bot(bot=True, reconnect=True, command_prefix="sv_prefix",
                      description="Interlinked")

if __name__ == "__main__":
    
    for cog in cogs:
        try:
            client.load_extension(cog)
            print("{} loaded without any problems.".format(cog))

        except Exception as e:
            print("Error loading cog %s" % cog)
            print("{}: {}".format(type(e).__name__, e))

f_cfg = open("data.json", 'r', encoding="utf8")
cfg = json.load(f_cfg)
f_cfg.close()

client.run(cfg["discord_key"])