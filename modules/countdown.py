from discord.ext import commands, tasks
from commons import loadFile, saveFile
import datetime 

class COUNTDOWNS(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.minutes.start()

    @commands.has_permissions(manage_channels=True)
    @commands.command(description="Command to add a coundown. Only for staff.", guild_only=True)
    async def addcountdown(self, ctx, *, arg):
        cfg = loadFile("info.json")
        countdowns = cfg["countdown"]
        args = arg.split(' ')
        print(args)
        if len(args) >= 2:
            name = ' '.join(args[2::])
            try:
                print(args[0])
                target = datetime.datetime.strptime(args[0], "%Y:%m:%d:%H:%M")
            except Exception:
                await ctx.send("I need this format \"YEAR:MONTH:DAY:HOUR:MINUTE\"")
                return
            
            try:
                newCountdown = {"utc": int(args[1]), "year": target.year, "month": target.month, "day": target.day, "hour": target.hour, "minute": target.minute}
            except ValueError:
                await ctx.send("UTCDiff must be a number.")
                return

            countdowns[str(ctx.channel.id)] = newCountdown 

            cfg["countdown"] = countdowns
            saveFile("info.json", cfg)

            if name:
                await ctx.send(f"The countdown for {name} has been set.")
            else:
                await ctx.send("The countdown has been set.")

        else: 
            await ctx.send("I need this format \"YEAR:MONTH:DAY:HOUR:MINUTE\" UTCDiff Name")

    @tasks.loop(seconds=301)
    async def minutes(self):
        cfg = loadFile("info.json")
        countdowns = cfg["countdown"]
        for x in countdowns:

            channel = self.client.get_channel(int(x))   
            print(channel)

            if channel:

                ctime = datetime.datetime.utcnow() + datetime.timedelta(hours=int(countdowns[x]["utc"]))

                year = countdowns[x]["year"]
                month = countdowns[x]["month"]
                day = countdowns[x]["day"]
                hour = countdowns[x]["hour"]
                minute = countdowns[x]["minute"]

                arg = f"{year}:{month}:{day}:{hour}:{minute}"
                target = datetime.datetime.strptime(arg, "%Y:%m:%d:%H:%M")
                diff = target-ctime 

                newName = f"{diff.days}d-{diff.seconds//3600}h-{(diff.seconds//60)%60}m"

                if diff.days <= -1:
                    await channel.send("THE COUNTDOWN IS OVER.")
                    del countdowns[x]
                    cfg["countdown"] = countdowns
                    saveFile("info.json", cfg)
                    await channel.edit(name="OVER")

                    return

                try:
                    await channel.edit(name=newName)
                except Exception as e:
                    print(e)


def setup(client):
    client.add_cog(COUNTDOWNS(client))