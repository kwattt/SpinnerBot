from discord.ext import commands
import discord
import traceback
import sys
# from https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612

class CommandErrorHandler(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.MissingPermissions):
            try:
                await ctx.send("<:hal9000:740607488138805351>")
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.MissingPermissions):
            try:
                await ctx.send("I need an argument <:hal9000:740607488138805351>")
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(client):
    client.add_cog(CommandErrorHandler(client))