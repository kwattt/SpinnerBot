from discord.ext import commands



class ROLES(commands.Cog):
    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(ROLES(client))