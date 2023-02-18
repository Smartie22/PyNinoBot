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
        self.latest = ''

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload_commands(self, ctx: commands.Context, file: str= None, path: str = 'cogs.commands'):
        """
        Reloads file using path to apply the most recent changes to the module
        wihtout affecting the runtime of the bot. Path defaults to cogs.commands
        if not provided
        usage: .reload <file: str> <path: str>
        """
        try:
            if not file and not self.latest:
                return await ctx.send("You didn't name a file to reload.")
            if not file and self.latest:
                self.bot.reload_extension(f'{self.latest}')
                return await ctx.send(f"`{self.latest.split('.')[-1]}` has been reloaded.")
            else:
                self.bot.reload_extension(f'{path}.{file}')
                self.latest = f'{path}.{file}'
                return await ctx.send(f"`{file}` has been reloaded.")
        except Exception:
            return await ctx.send(f"There was a problem and `{file}` has not been reloaded.")

def setup(bot):
    bot.add_cog(Reload(bot))