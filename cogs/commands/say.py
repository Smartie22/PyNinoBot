"""
This module is dedicated to the command 'say' which
will repeat what the user says and delete the original message
Creation Date: 19/02/2022
"""

from discord.ext import commands

class Say(commands.Cog):
    """
    This class handles the command say which
    will repeat what the user says and delete the original message
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='say')
    async def say(self, ctx: commands.Context, *, arg=''):
        await ctx.message.delete()
        if arg:
            return await ctx.send(arg)
        else:
            return await ctx.send("You didn't tell me anything to say.")

def setup(bot):
    bot.add_cog(Say(bot))
