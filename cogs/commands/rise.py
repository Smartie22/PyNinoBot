"""
This module is dedicated for the command 'rise' which sends
back a random Very Based Rise pic/gif
Creation Date: 09/04/2022
"""

import asyncio
from discord import Colour, Embed
from discord.ui import Button, View
from discord.ext import commands
from random import choice

class Rise(commands.Cog):
    """
    This class handles the main behaviour for the command 'rise'
    """

    def __init__(self, bot):
        self.bot = bot
        self.links = [
            'https://media.discordapp.net/attachments/835327750809452564/962404161532608592/1648666263091.jpg?width=453&height=670',
            'https://media.discordapp.net/attachments/835327750809452564/962404161285140530/IMG_20220403_033949.jpg?width=446&height=671',
            'https://media.discordapp.net/attachments/835327750809452564/962404160987365376/1649451311082.jpg?width=474&height=670',
            'https://media.discordapp.net/attachments/835327750809452564/962404161750724708/IMG_20220328_183030.jpg?width=451&height=669',
            'https://media.discordapp.net/attachments/835327750809452564/962404162207907940/1648328475723.jpg?width=501&height=669',
            'https://media.discordapp.net/attachments/835327750809452564/962450977967988836/20210130_003605.jpg?width=474&height=669',
        ]
        self.sent = []

    @commands.command(name='rise')
    async def rise(self, ctx: commands.Context):
        """
        Sends back a random link for a Rise Post
        usage: .rise
        """
        async def _pick_link():

            link = choice(self.links)

            while link in self.sent:
                link = choice(self.links)
                await asyncio.sleep(0)  # allows event loop to take back control temporarily

            self.sent.append(link)

            if len(self.sent) == len(self.links):
                self.sent = []
                self.sent.append(link)

            return link
        
        embed = Embed(title='The Very Based Rise Gallery:', description='Appreciate the very best idol, Rise Kujikawa!',
                      colour=Colour.gold()).set_image(url=await _pick_link())
        button = Button(emoji='🔄')
        view = View(button)

        async def button_random_callback(interaction):
            await interaction.message.edit(embed=embed.set_image(url= await _pick_link()))

        button.callback = button_random_callback
        await ctx.send(embed=embed, view=view)

def setup(bot):
    bot.add_cog(Rise(bot))