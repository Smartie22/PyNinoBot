"""
This module is dedicated for custom commands that can
be set up by the users
Creation Date: 21/04/2022
"""

from aiosqlite import connect

from discord.ext import commands

class CustomCommands(commands.Cog, name='custom commands'):
    """
    This lets you set up your very own customizable commands!
    Just tell me what response you want to link to that command and voila!
    You can even make them public so other people can use them too!
    I'm tired of using exclamation marks to induce excitement so just get on with it already and see for yourself. Jeesh.
    """

    def __init__(self, bot):
        self.bot = bot
    

    @commands.group(name='custom', aliases=('c', 'my'), invoke_without_command=True)
    async def custom(self, ctx: commands.Context, command: str | None = None):
        """
        Invoke your custom command anytime! Or look up all your commands in case your `[redacted]` head can't remember them all.
        That's why I'm here though so all good.

        Usage: 
        `.custom` to view all your commands.
        `.custom [command]` to invoke a command.
        Aliases: `c`, `my`
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
        """
        Add a new custom command to your name!

        Usage: 
        `.custom add [command] [response...]` to add a command.
        """
        async with connect('main.db') as db:
            async with db.cursor() as c:
                if not command:
                    await ctx.send('What are you expecting me to add? Your girlfriend? Oh wait...')
                elif args:
                    d = {'userid': ctx.author.id, 'username': ctx.author.name, 'command': command, 'content': ' '.join(args)}
                    await c.execute(f'INSERT INTO CustomCommands VALUES (:userid, :username, :command, 1, :content)', d)
                    await db.commit()
                    await ctx.send(f'the command `{command}` has been added successfully!')
                else:
                    await ctx.send("Nice empty command. Bet that'll be useful.")


    @custom.command(name='delete', aliases=('remove', 'del'))
    async def delete_custom(self, ctx:commands.Context, command: str | None = None):
        """
        Remove one of your commands in case you finally realized how terrible it truly was.

        Usage: 
        `.custom delete [command]` to delete a command.
        Aliases: `remove`, `del`
        """
        if command:
            async with connect('main.db') as db:
                async with db.cursor() as c:
                    d = {'userid': ctx.author.id, 'command': command}
                    await c.execute('''DELETE FROM CustomCommands WHERE userid = :userid AND command = :command 
                                       AND ROWID = (SELECT MAX(ROWID) FROM CustomCommands WHERE command = :command and userid = :userid)''', d)
                    await db.commit()
                    await ctx.send(f'The command `{command}` has been deleted successfully! ...if it existed and is yours. Kinda too lazy to check tbf.')
        else:
            await ctx.send("you didn't tell me what to delete :|")

    
    @custom.command(name= 'privacy', aliases=('priv', 'toggle'))
    async def toggle_privacy(self, ctx:commands.Context, command: str | None = None):
        """
        Toggle the privacy of your command to let other people use it or keep it to yourself like some weirdo command goblin.

        Usage: 
        `.custom privacy [command]` to toggle the privacy of a command.
        Aliases: `priv`, `toggle`
        """
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


    @custom.command(name='rename')
    async def rename(self, ctx:commands.Context, command: str | None = None, name: str | None = None):
        """
        Rename a command. That's it.
        Usage: 
        `.custom [command] [new_name]` to rename the command.
        """
        if command and name:
            d = {'userid': ctx.author.id, 'command': command, 'name': name}
            async with connect('main.db') as db:
                async with db.cursor() as c:
                    await c.execute('''SELECT command FROM CustomCommands WHERE userid = :userid AND command = :command 
                                 AND ROWID = (SELECT MAX(ROWID) FROM CustomCommands WHERE command = :command and userid = :userid)''', d)
                    result = await c.fetchone()
                    if result:
                        await c.execute('''UPDATE CustomCommands SET command = :name WHERE command = :command AND userid = :userid
                                    AND ROWID = (SELECT MAX(ROWID) FROM CustomCommands WHERE command = :command and userid = :userid)''', d)
                        await db.commit()
                        await ctx.send(f'The command `{command}` has been renamed to `{name}`.')
                    else:
                        await ctx.send('There is no such command...')
        else:
            await ctx.send('You need to pass two names :|')

    
    @custom.command(name='update')
    async def update(self, ctx:commands.Context, command: str | None = None, *content):
        """
        Update the content of the custom command in case you messed up like you always do.
        Usage: 
        `.custom [commant] [new_response...]` to update the command.
        """
        d = {'userid': ctx.author.id, 'command': command, 'content': ' '.join(content)}
        if not command:
            await ctx.send("Can't update nothing so try giving an actual command next time.")
        elif content:
            async with connect('main.db') as db:
                async with db.cursor() as c:
                    await c.execute('''SELECT content FROM CustomCommands WHERE userid = :userid AND command = :command 
                                AND ROWID = (SELECT MAX(ROWID) FROM CustomCommands WHERE command = :command and userid = :userid)''', d)
                    result = await c.fetchone()
                    if result:
                        await c.execute('''UPDATE CustomCommands SET content = :content WHERE command = :command AND userid = :userid
                                    AND ROWID = (SELECT MAX(ROWID) FROM CustomCommands WHERE command = :command and userid = :userid)''', d)
                        await db.commit()
                        await ctx.send(f'The command `{command}` has been updated.')
                    else:
                        await ctx.send('There is no such command...')
        else:
            await ctx.send("Nice empty command. Bet that'll be useful.")


def setup(bot):
    bot.add_cog(CustomCommands(bot))