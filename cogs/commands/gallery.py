"""
This module is dedicated for the gallery command which sends
back an embed for an art gallery of a character.
Creation Date: 09/04/2022
"""

import asyncio
from discord import Colour, Embed
from discord.ui import Button, View
from discord.ext import commands
from random import choice

class GalleryCog(commands.Cog, name='gallery'):
    """
    Lets me show you a very cool, epic and cute collection of the topest of top tier art, which I have personally curated!
    """

    def __init__(self, bot):
        self.bot = bot
        self._rise = [
            'https://media.discordapp.net/attachments/835327750809452564/962404161532608592/1648666263091.jpg?width=453&height=670',
            'https://media.discordapp.net/attachments/835327750809452564/962404161285140530/IMG_20220403_033949.jpg?width=446&height=671',
            'https://media.discordapp.net/attachments/835327750809452564/962404160987365376/1649451311082.jpg?width=474&height=670',
            'https://media.discordapp.net/attachments/835327750809452564/962404161750724708/IMG_20220328_183030.jpg?width=451&height=669',
            'https://media.discordapp.net/attachments/835327750809452564/962404162207907940/1648328475723.jpg?width=501&height=669',
            'https://media.discordapp.net/attachments/835327750809452564/962450977967988836/20210130_003605.jpg?width=474&height=669',
        ]
        self.sent = []

    @commands.group(name='gallery', invoke_without_command=True)
    async def gallery(self, ctx:commands.Context):
        """
        Shows all characters who have their own art gallery.

        Usage: 
        `.gallery` to list the galleries.
        """
        g = ['`Rise Kujikawa`']
        return await ctx.send("Here are the available galleries : " + ', '.join(g))

    @gallery.command(name='rise')
    async def rise(self, ctx: commands.Context):
        """
        Sends the art gallery for Rise Kujikawa!

        Usage: 
        `.gallery rise` to show Rise's Gallery.
        """
        async def _pick_link():

            link = choice(self._rise)

            while link in self.sent:
                link = choice(self._rise)
                await asyncio.sleep(0)  # allows main event loop to keep going

            self.sent.append(link)

            if len(self.sent) == len(self._rise):
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
    bot.add_cog(GalleryCog(bot))