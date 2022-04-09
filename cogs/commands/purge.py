"""
This module is dedicated for the owner-only command 'purge'
which deletes a number of messages from the channel it was called in
Creation Date: 04/11/2021
"""

from discord.ext import commands

class Purge(commands.Cog):
    """
    This class handles the owner only command 'purge'
    which deletes a number of messages from the channel it was called in
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='purge')
    @commands.is_owner()
    async def purge_messsages(self, ctx: commands.Context, number_of_messages: int =1):
        """
        Purges a number_of_messages from the channel it was called from or the last
        message if not given a number
        usage: .purge <number_of_messages>
        """
        try:
            if number_of_messages > 100:
                return await ctx.send("That's too many messages at once!")
            print(f'{number_of_messages} message(s) deleted from {ctx.channel}')
            await ctx.channel.purge(limit=number_of_messages + 1, check=lambda msg: not msg.pinned)
        except Exception:
            await ctx.send("You can't use that!")

def setup(bot):
    bot.add_cog(Purge(bot))