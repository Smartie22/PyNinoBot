# This is the 'Nino Bot' by Mark Aziz (formerly the Itsuki Bot)'
# Started development on 23-04-2021
# She is a super good girl (unstoppable train) just so you know so i'm planning
# to add a ton of functionality and make her dominate your heart too!

import os
import random
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')

bot = commands.Bot(command_prefix='Nino, ')

@bot.event
# this funtion runs when Nino makes a successful connection to discord
async def on_ready():
    guilds = bot.guilds
    
    for guild in guilds:
        print(f'{bot.user} has done the thing on {guild.name}!!\nit also got the number {guild.id}??\nwhat an ominous number...\n')

        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')
# end of on_ready()

@bot.event
# this funtion reads the latest message and if it has 'nino' in it,
# it will reply back
# special lines if the author's id matches mark
async def on_message(message):
    if message.author == bot.user:
        return

    greetings =  [
        'HIIII, I\'M ITSUKI!!!',
        'HIIII, I\'M ITSUKI! NICE TO MEET YOU TOOOO!!',
        'HIIII, THAT\'S MEEE!! HOW ARE YOU DOING TODAY!!'
    ]

    if 'itsuki' in message.content.lower() and not 'Itsuki, ' in message.content:
        if message.author.id == 247071316686012416:
            if 'i love you' in message.content.lower():
                await message.channel.send('HIII MARK!!! I LOVE YOUUU TOOO!!!! <3 <3 <3')
            else:
                await message.channel.send('HIII MARK!!! I LOVE YOU SOOO MUCH!!!! <3 <3 <3')
        
        else:
            response = random.choice(greetings)
            await message.channel.send(response)
    await bot.process_commands(message)
#end of on_message()

@bot.command()
async def here(ctx):
    await ctx.send('HI HI HI!!! I\'M HERE TO HELP!!!')

bot.run(TOKEN)