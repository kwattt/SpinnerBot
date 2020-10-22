from discord.ext import commands
from commons import loadFile, saveFile
from discord import Embed

class MISC(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_permissions(manage_roles=True)
    @commands.command(description="Command to change prefix. Available only for staff.")
    async def spinprefix(self, ctx, arg):
        emb = Embed(title="Help & commands", description=
        '''


        '''
        , color=0xe78b2e)


def setup(client):
    client.add_cog(MISC(client))