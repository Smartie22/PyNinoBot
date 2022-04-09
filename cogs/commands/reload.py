"""
This module is dedicated for the owner-only command 'reload'
which reloads the command it was invoked with to apply the latest
changes without affecting the runtime of the bot
Creation Date: 18/01/2022
"""

from discord.ext import commands

class Reload(commands.Cog):
    """
    This class handles the owner-only command 'reload'
    which reloads the command it was invoked with to apply the latest
    changes without affecting the runtime of the bot
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reload')
    @commands.is_owner()
    async def reload_commands(self, ctx: commands.Context, file: str, path: str = 'cogs.commands'):
        """
        Reloads file using path to apply the most recent changes to the module
        wihtout affecting the runtime of the bot. path defaults to cogs.commands
        if not provided
        usage: .reload <file: str> <path: str>
        """
        try:
            self.bot.reload_extension(f'{path}.{file}')
            return await ctx.send(f"{file} has been reloaded.")
        except:
            return await ctx.send(f"There was a problem and {file} has not been reloaded.")

def setup(bot):
    bot.add_cog(Reload(bot))