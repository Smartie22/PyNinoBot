"""
This module is dedicated for the Rock Paper Scissors game command system
Creation date: 04/11/2021
"""

import random
import asyncio
from discord.ext import commands

class RPS(commands.Cog):
    """
    This class handles the rock paper scissors minigame
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='rps')
    async def rps(self, ctx: commands.Context, *input):
        rps_choices = ('rock', 'paper', 'scissors')
        bot_score = 0
        user_score = 0
        again = True
        if input == ():
            await ctx.send(f"Oh {str(ctx.author)[:-5]}, You wanna play against me in Rock, Paper, Scissors? \nAlright")
            while again:
                await ctx.send("What're you gonna choose?")

                def check_choice(m):
                    return ctx.author == m.author and ctx.channel == m.channel \
                        and m.content.lower().strip() in rps_choices

                try:
                    user_choice = await self.bot.wait_for('message',timeout=30.0,check=check_choice)
                    user_choice = user_choice.content.lower().strip()

                    bot_choice = random.choice(rps_choices)

                    await ctx.send(f"I chose {bot_choice}")

                    if bot_choice == user_choice:
                        await ctx.send(f"Aww, it's a draw.")

                    elif (bot_choice == rps_choices[0] and user_choice == rps_choices[1]) \
                        or (bot_choice == rps_choices[1] and user_choice == rps_choices[2]) \
                        or (bot_choice == rps_choices[2] and user_choice == rps_choices[0]):
                        
                        await ctx.send("Pft. You just got lucky. Fine, you win this one.")
                        user_score += 1

                    elif bot_choice == rps_choices[0] and user_choice == rps_choices[2] \
                        or bot_choice == rps_choices[2] and user_choice == rps_choices[1] \
                            or bot_choice == rps_choices[1] and user_choice == rps_choices[0]:
                        
                        await ctx.send("Hehe, I won. Not surprising.")
                        bot_score += 1

                    await ctx.send(f"My score is {bot_score} and yours is {user_score}")
                    await ctx.send(f"Wanna play again?")

                    def check_again(m):
                        return ctx.author == m.author and ctx.channel == m.channel and \
                            m.content.lower().strip() in ('yes','no', 'y', 'n', 'ye', 'nah', 'na')

                    try:
                        again = await self.bot.wait_for('message', timeout=30.0, check=check_again)
                        again = again.content.lower().strip()

                    except asyncio.TimeoutError:
                        await ctx.send('Rock, Paper, Scissors timed out')


                except asyncio.TimeoutError:
                    await ctx.send('Rock, Paper, Scissors timed out')

                if again in ('yes', 'y'):
                    again = True
                else:
                    again = False
                    if bot_score == user_score:
                        await ctx.send(f"Alright!\nMy score was {bot_score} and yours was {user_score}\nI won't go easy on you next time!")
                    elif bot_score > user_score:
                        await ctx.send(f"Alright!\nMy score was {bot_score} and yours was {user_score}\nBetter luck next time!")
                    else:
                        await ctx.send(f"Alright!\nMy score was {bot_score} and yours was {user_score}\nJust know I won't lose to you again!")

def setup(bot):
    bot.add_cog(RPS(bot))