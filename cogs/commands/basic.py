"""
This module will contain the cog that manages all basic commands
Creation Date: 16/02/2023
"""

import time

from discord.ext import commands


class BasicCog(commands.Cog, name='basic'):
    """
    These are simple commands which aren't nearly as cool as my other stuff but it's still nice to have them, I suppose.
    """

    @commands.command(name='ping')
    
    async def ping(self, ctx: commands.Context):
        """
        A basic ping command to check latency and API response times.

        Usage: 
        `.ping` to send the ping message.
        """
        start_time = time.time()
        message = await ctx.send("Testing ping...")
        end_time = time.time()
        await message.edit(content=(
            f"Pong!\nThe websocket latency is {round((self.bot.latency)*1000)}ms\n\
            The API latency is {round((end_time-start_time)*1000)}ms"
        ))

    @commands.command(name='echo')
    async def echo(self, ctx: commands.Context, *, arg=''):
        """
        An echo command which makes me repeat what you tell me. Very useful, I know.
        
        Usage: 
        `.echo [something...]` to echo something.
        """
        if arg:
            return await ctx.send(arg)
        else:
            return await ctx.send("You didn't tell me anything to echo.")
        
    @commands.command(name='send')
    async def send(self, ctx: commands.Context, *, arg=''):
        """
        A send command which makes me send something and delete your message as if you never told me to send anything.
        Slightly more useful and much funnier than echo.

        Usage: 
        `.send [something...]` to send something
        """
        if arg:
            await ctx.send(arg)
            return await ctx.message.delete()
        else:
            return await ctx.send("You didn't tell me anything to say.")



def setup(bot):
    bot.add_cog(BasicCog(bot))