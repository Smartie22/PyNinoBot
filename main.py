"""
This is the 'Nino Bot', Master bot of the Wisteria Studios bot system, by Mark Aziz
Started development on 23/04/2021
She is a super good girl (unstoppable train) just so you know so i'm planning
to add a ton of functionality and make her dominate your heart too!
"""

import os
import logging
from dotenv import load_dotenv

import discord
from discord.flags import Intents
from discord.ext import commands

# sets up the logger to log to a file named discord.log
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# sets up the intents to be used by the bot
intents = Intents.default()
intents.guild_messages = True
intents.members = True
intents.typing = False
intents.presences = False

# load the environmental variables from .env
load_dotenv()
TOKEN = os.getenv('NINO_TOKEN')
GUILD = os.getenv('GUILD')
OWNER = int(os.getenv('OWNER'))
CHANNEL = os.getenv('CHANNEL')

bot = commands.Bot(command_prefix=('.', '!'), owner_id=OWNER, case_insensitive=True, strip_after_prefix=True, intents=intents)
cog_path = 'cogs.commands'
cog_files = [f'{cog_path}.rps',
             f'{cog_path}.reload',
             f'{cog_path}.purge',
             f'{cog_path}.ping',
             f'{cog_path}.echo',
             f'{cog_path}.say',
             f'{cog_path}.rise'
            ]


@bot.event
async def on_ready():
    """Runs when bot first makes connection to the API"""
    for guild in bot.guilds:
        print(f'{bot.user.name.upper()} FINALLY LANDED ON {str(guild).upper()}!!')

 # runs the code using the bot account through the token

if __name__ == "__main__":
    for cog_file in cog_files:
        bot.load_extension(cog_file)
        
bot.run(TOKEN)