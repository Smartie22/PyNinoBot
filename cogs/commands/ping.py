"""
This module is dedicated to the command 'ping' which sends
info about latency
Creation date: 04/11/2021
"""

import time
from discord.ext import commands

class Ping(commands.Cog):
    """
    This class is dedicated to the command 'ping' which sends
    info about latency
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='ping')
    async def ping(self, ctx: commands.Context):
        start_time = time.time()
        message = await ctx.send("Testing ping...")
        end_time = time.time()
        await message.edit(content=f"Pong!\n\
The websocket latency is {round((self.bot.latency)*1000)}ms\n\
The API latency is {round((end_time-start_time)*1000)}ms")

def setup(bot):
    bot.add_cog(Ping(bot))