"""
This module is dedicated for custom commands that can
be set up by the users
Creation Date: 21/04/2022
"""

from aiosqlite import connect

from discord.ext import commands

class CustomCommands(commands.Cog):
    """
    This class handles all commands for custom commands
    """

    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name='custom', aliases=('c', 'my'), invoke_without_command=True)
    async def custom(self, ctx: commands.Context, command: str | None = None):
        """
        Set your very own commands!
        """
        async with connect('main.db') as db:
            if command:
                async with db.cursor() as privcur:
                    d = {'userid': ctx.author.id, 'username': ctx.author.name, 'command': command}
                    await privcur.execute('SELECT content, username FROM CustomCommands WHERE userid = :userid AND command = :command', d)
                    result = await privcur.fetchone()
                    if result:
                        await ctx.send(result[0])
                        if ctx.author.name != result[1]:
                            await privcur.execute('UPDATE CustomCommands SET username = :username WHERE userid = :userid', d)
                    else:
                        async with db.cursor() as pubcur:
                            await pubcur.execute('SELECT content, username FROM CustomCommands WHERE privacy = 0 AND command = :command', d)
                            result = await pubcur.fetchone()
                            if result:
                                await ctx.send(result[0])
                                if ctx.author.name != result[1]:
                                    await pubcur.execute('UPDATE CustomCommands SET username = :username WHERE userid = :userid', d)
                            else:
                                await ctx.send('There is no such command...')
            else:
                async with db.cursor() as privcur:
                    d = {'userid': ctx.author.id}
                    await privcur.execute('SELECT command FROM CustomCommands WHERE userid = :userid', d)
                    # adds all elements in every row in the fetched set
                    commands_list = [c for row in (await privcur.fetchall()) for c in row] 
                    m = 'These are all your custom commands: `' + '`, `'.join(commands_list) + ' `'
                async with db.cursor() as pubcur:
                    await pubcur.execute('SELECT command FROM CustomCommands WHERE privacy = 0')
                    commands_list = [c for row in (await pubcur.fetchall()) for c in row]
                    m2 = 'These are all public custom commands: `' + '`, `'.join(commands_list) + ' `'
                    await ctx.send(m + '\n' + m2)


    @custom.command(name='add')
    async def add_custom(self, ctx:commands.Context, command: str | None = None, *args):
        async with connect('main.db') as db:
            async with db.cursor() as c:
                if not command:
                    await ctx.send('What are you expecting me to add? Your girlfriend?')
                elif args:
                    d = {'userid': ctx.author.id, 'username': ctx.author.name, 'command': command, 'content': ' '.join(args)}
                    await c.execute(f'INSERT INTO CustomCommands VALUES (:userid, :username, :command, 1, :content)', d)
                    await db.commit()
                    await ctx.send(f'the command `{command}` has been added successfully!')
                else:
                    await ctx.send('Nice empty command. Bet that\'ll be useful.')


    @custom.command(name='delete', aliases=('remove', 'del'))
    async def delete_custom(self, ctx:commands.Context, command: str | None = None):
        if command:
            async with connect('main.db') as db:
                async with db.cursor() as c:
                    d = {'userid': ctx.author.id, 'command': command}
                    await c.execute('''DELETE FROM CustomCommands WHERE userid = :userid AND command = :command 
                                       AND ROWID = (SELECT MAX(ROWID) FROM CustomCommands WHERE command = :command and userid = :userid)''', d)
                    await db.commit()
                    await ctx.send(f'The command `{command}` has been deleted successfully! ...if it existed and is yours.')
        else:
            await ctx.send("you didn't tell me what to delete :|")
    
    @custom.command(name= 'privacy', aliases=('priv', 'toggle'))
    async def toggle_privacy(self, ctx:commands.Context, command: str | None = None):
        if command:
            d = {'userid': ctx.author.id, 'command': command}
            async with connect('main.db') as db:
                async with db.cursor() as c:
                    await c.execute('''SELECT command, privacy FROM CustomCommands WHERE userid = :userid AND command = :command 
                                 AND ROWID = (SELECT MAX(ROWID) FROM CustomCommands WHERE command = :command and userid = :userid)''', d)
                    result = await c.fetchone()
                    if result:
                        if result[1] == 1:
                            await c.execute('''UPDATE CustomCommands SET privacy = 0 WHERE command = :command AND userid = :userid
                                        AND ROWID = (SELECT MAX(ROWID) FROM CustomCommands WHERE command = :command and userid = :userid)''', d)
                            await db.commit()
                            await ctx.send(f'The command `{command}` has been toggled to public.')
                        else:
                            await c.execute('''UPDATE CustomCommands SET privacy = 1 WHERE command = :command AND userid = :userid
                                        AND ROWID = (SELECT MAX(ROWID) FROM CustomCommands WHERE command = :command and userid = :userid)''', d)
                            await db.commit()
                            await ctx.send(f'The command `{command}` has been toggled to private.')
                    else:
                        await ctx.send('There is no such command...')
        else:
            d = {'userid': ctx.author.id, 'command': command}
            async with connect('main.db') as db:
                async with db.cursor() as c:
                    await c.execute('''SELECT command, privacy FROM CustomCommands WHERE userid = :userid
                                 AND ROWID = (SELECT MAX(ROWID) FROM CustomCommands WHERE userid = :userid)''', d)
                    result = await c.fetchone()
                    if result:
                        if result[1] == 1:
                            await c.execute('''UPDATE CustomCommands SET privacy = 0 WHERE userid = :userid
                                        AND ROWID = (SELECT MAX(ROWID) FROM CustomCommands WHERE userid = :userid)''', d)
                            await db.commit()
                            await ctx.send(f'The command `{result[0]}` has been toggled to public.')
                        else:
                            await c.execute('''UPDATE CustomCommands SET privacy = 1 WHERE userid = :userid
                                        AND ROWID = (SELECT MAX(ROWID) FROM CustomCommands WHERE userid = :userid)''', d)
                            await db.commit()
                            await ctx.send(f'The command `{result[0]}` has been toggled to private.')
                    else:
                        await ctx.send('There is no such command...')

def setup(bot):
    bot.add_cog(CustomCommands(bot))