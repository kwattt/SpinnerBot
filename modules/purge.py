from discord.ext import commands, tasks
from commons import loadFile, saveFile
from datetime import datetime, timedelta
from pytz import timezone, UTC

class PURGE(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.to_keep = []

    @commands.Cog.listener()
    async def on_ready(self):
        self.minutes.start()

    @tasks.loop(seconds=60)
    async def minutes(self):

        purge = loadFile("info.json")["purge"]

        for c_purge in purge:
            channel = self.client.get_channel(int(c_purge["channel"]))   
            if not channel:
                continue

            if not "type" in c_purge.keys() or c_purge["type"] == 0:
                ctime = datetime.now(timezone("Etc/UTC"))
                future = datetime.now(timezone("Etc/UTC")) + timedelta(minutes=15)

                if c_purge["hour"] == future.hour and c_purge["minute"] == future.minute:
                    await channel.send("-- This channel will be purged in 15 minutes --")

                elif c_purge["hour"] == ctime.hour and c_purge["minute"] == ctime.minute:
                    await channel.purge(limit=9999)
                    await channel.send("This channel has been purged.")
                    await channel.send("The next Purge will occur every day at {}:{} UTC-0".format(ctime.strftime('%H'), ctime.strftime('%M')))

            elif c_purge["type"] == 1:
                current_timestamp = datetime.now()

                bulk=[]
                async for message in channel.history():
                    if current_timestamp.timestamp() >= (message.created_at + timedelta(hours=24)).timestamp() and not message.pinned:
                        bulk.append(message)

                await channel.delete_messages(bulk)

    @commands.has_permissions(manage_channels=True)
    @commands.command(description="Command to purge the current channel", guild_only=True)
    async def deletechannel(self, ctx):
        if ctx.message.author.guild_permissions.manage_roles: 
            channel = ctx.channel
            await channel.purge(limit=99999)
            await channel.send("This channel has been purged.")
        else: 
            await ctx.send("<:hal9000:740607488138805351>")

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
                await ctx.send("I need this format \"MINUTE:HOUR\" ")
                return 

            if not str(cid) in purge:            
                if target:
                    newpurge = {"channel": cid, "hour": target.hour, "minute": target.minute}
                    purge[str(cid)] = newpurge 
                    await ctx.send("I will purge this channel every day at {}:{} UTC-0".format(target.hour, target.minute))
                    cfg["purge"] = purge
                    saveFile("info.json", cfg)
                else: 
                    await ctx.send("I need this format \"MINUTE:HOUR\" ")
            else: 
                del purge[str(cid)]
                cfg["purge"] = purge
                saveFile("info.json", cfg)
                await ctx.send("Purge has been disabled for this channel.")
        else:
            if str(cid) in purge:            
                del purge[str(cid)]
                cfg["purge"] = purge
                saveFile("info.json", cfg)
                await ctx.send("Purge has been disabled for this channel.")

async def setup(client):
    await client.add_cog(PURGE(client))