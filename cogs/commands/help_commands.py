"""
This module is dedicated to the help commands
Creation Date: 15/01/2023
"""
from typing import Set
from discord import Embed

from discord.ext import commands

class CustomHelp(commands.HelpCommand):


    async def _send_embed(self, title: str, description: str = None, mapping: dict = None, commands: Set[commands.Command] = None):
        embed = Embed(title=title,
                      description=description if description else '',
                      colour=0xed6ad5)

        if commands:
            commands = await self.filter_commands(commands)

            for command in commands:
                embed.add_field(name=command.qualified_name,
                                value=command.short_doc,
                                inline=False)
                
        elif mapping:
            # if mapping is not None then this is a general help command so list all commands and their groups
            for cog, commands in mapping.items():
                commands = await self.filter_commands(commands)
                if not commands: continue
                
                name = cog.qualified_name.capitalize() if cog else ""

                cmd_list = "\u2002".join(f"`{cmd.name}`" for cmd in commands)

                value = f"{cog.description}\n{cmd_list}" if cog and cog.description else cmd_list

                embed.add_field(name=name, value=value, inline=False)
            
            embed.set_thumbnail(url=self.context.bot.user.display_avatar)

        return await self.get_destination().send(embed=embed)
        

    async def send_bot_help(self, mapping):
        return await self._send_embed(title="My Command List!",
                                      description="These are my commands that you can use to be the coolest kid in Wisteria Studios!",
                                      mapping=mapping)



    async def send_command_help(self, command: commands.Command):
        return await self._send_embed(title=command.qualified_name,
                                      description=command.help,
                                      commands = command.commands if isinstance(command, commands.Group) else None)



    async def send_group_help(self, group):
        return await self.send_command_help(group)



    async def send_cog_help(self, cog: commands.Cog):
        return await self._send_embed(title=cog.qualified_name,
                                      description=cog.description,
                                      commands=cog.get_commands())












class Help(commands.Cog):
    """
    The know-it-all command that will show you everything you need to know about my commands!
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.help_command = CustomHelp()
        bot.help_command.cog = self
    

def setup(bot):
    bot.add_cog(Help(bot))