from discord.ext import commands
from commons import loadFile
from discord import Embed
import datetime

class MENTIONS(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.channel = loadFile("info.json")["mentionChannel"]

    @commands.Cog.listener()
    async def on_message(self, msg): 
        mentions = msg.role_mentions
        if mentions:
            target_channel = self.client.get_channel(int(self.channel))
            if target_channel:

                values = "" 
                for role in mentions:
                    values += role.name + " " 

                values += "\n"
                values += f"\n**In channel:**  {msg.channel.name}"

                uname = f"{msg.author.nick} ({msg.author.name}#{msg.author.discriminator})"

                embed = Embed(title="Mentioned roles", description=values, timestamp=datetime.datetime.utcnow(), colour=0x22b7ba)

                embed.set_author(name=uname, icon_url=msg.author.avatar_url)

                uid = f"user id: {msg.author.id} "
                
                embed.set_footer(text=uid)
                await target_channel.send(embed=embed)


def setup(client):
    client.add_cog(MENTIONS(client))