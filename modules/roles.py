import discord
from discord.ext import commands
from commons import loadFile, saveFile
from discord import Embed


class ROLES(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Displays available custom booster color roles.", guild_only=True)
    async def boostercolors(self, ctx):
        roles = loadFile("info.json")["roles"]
        colors = ""
        for x in roles:
            colors += x + "\n"
        emb = Embed(title="Colors", description=colors, color=0xe78b2e)
        await ctx.send(embed=emb)

    async def remove_roles(self, ctx):
        roless = loadFile("info.json")["roles"]
        for role in ctx.author.roles:
            if role.name in  roless:
                await ctx.author.remove_roles(role)
                break

    @commands.command(description="Assign a custom color role. Only available for Server Boosters.", aliases=['rboostercolor'], guild_only=True)
    async def boostercolor(self, ctx, arg):
        # check if user is a booster
        if discord.utils.get(ctx.guild.roles, name="Server Booster") in ctx.author.roles:
            if arg:
                roles = loadFile("info.json")["roles"]
                if arg.lower() in [rol.lower() for rol in roles]:
                    idx = [rol.lower() for rol in roles].index(arg.lower())
                    # it exists, lets search for it.
                    role = discord.utils.get(ctx.guild.roles, name=roles[idx])
                    if role:

                        # does the user have the role?                        
                        if not role in ctx.author.roles: 
                            await self.remove_roles(ctx)
                            await ctx.author.add_roles(role)
                            await ctx.send("You now have the role " + arg)
                        else:
                            await ctx.author.remove_roles(role)
                            await ctx.send("You no longer have the role " + arg)
                    else:
                        await ctx.send("<:hal9000:740607488138805351>")
                else:
                    await ctx.send("<:hal9000:740607488138805351>")
            else:
                await ctx.send("<:hal9000:740607488138805351>")
        else: 
            await ctx.send("This command is only available for Server Boosters.")

    @commands.has_permissions(manage_roles=True)
    @commands.command(description="Command to add roles. Available only for staff.", guild_only=True)
    async def addboostercolor(self, ctx, arg):
        if ctx.message.author.guild_permissions.manage_roles: # added my id for testing
            cfg = loadFile("info.json")
            roles = cfg["roles"]
            if arg: 
                role = discord.utils.get(ctx.guild.roles, name=arg)
                if role:
                    if not arg in roles:
                        await ctx.send("Added " + arg + " to the role list.")
                        roles.append(arg)
                        cfg["roles"] = roles
                        saveFile("info.json", cfg)
                    else:
                        await ctx.send("Removed " + arg + " from the role list.")
                        roles.remove(arg)
                        cfg["roles"] = roles
                        saveFile("info.json", cfg)
                else:
                    await ctx.send("<:hal9000:740607488138805351>")
            else:
                await ctx.send("<:hal9000:740607488138805351>")
        else:
            await ctx.send("<:hal9000:740607488138805351>")

def setup(client):
    client.add_cog(ROLES(client))