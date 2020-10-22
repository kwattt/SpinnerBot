from discord.ext import commands, tasks
from commons import loadFile, saveFile
from datetime import datetime
from pytz import timezone

class PURGE(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.minutes.start()

    @tasks.loop(seconds=60)
    async def minutes(self):
        ctime = datetime.now(timezone("Etc/UTC"))
        purge = loadFile("info.json")["purge"]
        for b in purge:
            if purge[b]["hour"] == ctime.hour and purge[b]["minute"] == ctime.minute:
                cid = purge[b]["channel"]
                channel = self.client.get_channel(cid)   
                await channel.purge(limit=9999)
                await channel.send("This channel has been purged.")
                await channel.send("The next Purge will occur every day at {}:{} UTC-0".format(ctime.hour, ctime.minute))

    @commands.has_permissions(manage_channels=True)
    @commands.command(description="Command to purge this channel at a  specified time.", guild_only=True)
    async def purgechannel(self, ctx, arg=None):
        cfg = loadFile("info.json")
        purge = cfg["purge"]
        cid = ctx.channel.id
        if arg:
            try: 
                target = datetime.strptime(arg, "%H:%M")
            except ValueError:
                await ctx.send("I need this format \"MINUTE-HOUR\" ")
                return 

            if not cid in purge:            
                if target:
                    newpurge = {"channel": cid, "hour": target.hour, "minute": target.minute}
                    purge[cid] = newpurge 
                    await ctx.send("I will purge this channel every day at {}:{} UTC-0".format(target.hour, target.minute))
                    cfg["purge"] = purge
                    saveFile("info.json", cfg)
                else: 
                    await ctx.send("I need this format \"MINUTE-HOUR\" ")
            else: 
                del purge[cid]
                cfg["purge"] = purge
                saveFile("info.json", purge)
                await ctx.send("Purge has been disabled for this channel.")
        elif cid in purge:            
            del purge[cid]
            cfg["purge"] = purge
            saveFile("info.json", purge)
            await ctx.send("Purge has been disabled for this channel.")

    @commands.command(description="Command to check the remaining time to purge a channel.", guild_only=True)
    async def purgetime(self, ctx):
        cid = ctx.channel.id
        purges = loadFile("info.json")["purge"]
        if str(cid) in purges:
            ctime = datetime.now(timezone("Etc/UTC"))
            rhour = abs(24+purges[str(cid)]["hour"] - ctime.hour)
            rminute = abs(purges[str(cid)]["minute"] - ctime.minute)
            await ctx.send("This channel will be purged in {} hours and {} minutes".format(rhour, rminute))
        else:
            await ctx.send("Purge is not enabled for this channel.")

def setup(client):
    client.add_cog(PURGE(client))