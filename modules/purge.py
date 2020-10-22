from discord.ext import commands
from commons import loadFile, saveFile
from discord import Embed

class PURGE(commands.Cog):
    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(PURGE(client))