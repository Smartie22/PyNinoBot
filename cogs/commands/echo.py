"""
this module is dedicated to the command 'echo' 
which echoes what the user says after
Creation Date: 04/11/2021
"""
import discord
from discord.ext import commands

class Echo(commands.Cog):
    """
    This class handles the command 'echo' which
    echoes what the user says after
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='echo')
    async def echo(self, ctx: commands.Context, *, arg=''):
        if arg:
            return await ctx.send(arg)
        else:
            return await ctx.send("You didn't tell me anything to echo.")

def setup(bot):
    bot.add_cog(Echo(bot))