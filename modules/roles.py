import discord
from discord.ext import commands
from commons import loadFile, saveFile

class ROLES(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="To change your role, only boosters btw.")
    async def roleb(self, ctx, arg):
        # check if user is a booster

        if discord.utils.get(ctx.guild.roles, name="Server Booster") in ctx.author.roles:
            if arg: 
                roles = loadFile("info.json")["roles"]
                if arg in roles:
                    # it exists, lets search for it.
                    role = discord.utils.get(ctx.guild.roles, name=arg)
                    if role:
                        await ctx.author.add_roles(role)
                        ctx.send("Now you are " + arg)
                    else: 
                        print("hmm")
            else:
                ctx.send("<:hal9000:768633142504325130>")
        else: 
            ctx.send("I'm going to need :money_with_wings:")

def setup(client):
    client.add_cog(ROLES(client))