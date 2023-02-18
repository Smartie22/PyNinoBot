"""
This module is dedicated for music commands that can
be used to play music in voice channels by the users
Creation Date: 15/01/2023
"""
import discord
from asyncio import Queue, sleep
import logging

from yt_dlp import YoutubeDL

from discord.ext import commands
from discord.embeds import Embed

class MusicCog(commands.Cog, name='music'):
    """
    The Ultimate Music-In-VC Player! Who would have guessed that it was me all along!
    Lets me play videos from youtube in your voice channel. Something other... inferior Music-In-VC players can't do.
    Who can blame them though, they're just NPCs.
    """
    def __init__(self, bot: commands.Bot):

        logger = logging.getLogger('ydl')
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(filename='ydl.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(handler)

        self.bot = bot
        self.dl_opts = {
                    'format': 'bestaudio',
                    'format-sort': '+abr',
                    'logger': logger,
                }
        self.ffmpeg_opts = {
                    'options': '-vn',
                    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                }
        
        self.queue = Queue(1)
        self.current = {}
        self.lqueue = []
        self._loop = 0


    @commands.command(name='play', aliases=['p'])
    async def play(self, ctx: commands.Context, *, search: str =''):
        """
        Play whatever you want in your voice channel! 
        You can give me a name, a link, a youtube video ID if you for whatever reason decided to use that instead of literally anything else.

        Usage: 
        `.play [search]` to search and play.
        `.play` to resume from a pause.
        Alias: `p`
        """
        if not search == '':
            vc = None
            try:
                # checks the channel the user is in
                vc:discord.VoiceChannel = discord.utils.get(ctx.message.guild.voice_channels, name=ctx.message.author.voice.channel.name)
            except AttributeError:
                return await ctx.send("You're not in a voice channel. Who am I going to play to...")
            
            voice:discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.message.guild)

            await self.queue_next_song(ctx, search)

            # if not connected then connect and if connected ensure the connection is to the right vc
            try:
                voice:discord.VoiceClient = await vc.connect()
                await self.play_next_song(ctx, voice)
            except discord.ClientException:
                voice:discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.message.guild)

            if voice and vc != voice.channel:
                await voice.move_to(vc)

        elif not search:
            try:
                # manages resumes
                vc =  discord.utils.get(ctx.message.guild.voice_channels, name=ctx.message.author.voice.channel.name)
                voice = discord.utils.get(self.bot.voice_clients, guild=ctx.message.guild)
                if not voice:
                    return await ctx.send("I can't play nothing :|")
                if voice.is_paused():
                    voice.resume()
                else:
                    return await ctx.send("I can't play nothing :|")
            except AttributeError:
                return await ctx.send("You're not in a voice channel. Who am I going to play to...")


    @commands.command(name='pause')
    async def pause(self, ctx: commands.Context):
        """
        Pause the music I am currently playing. That simple.

        Usage: 
        `.pause` to pause.
        """
        try:
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            if voice.is_playing():
                voice.pause()
            else:
                return await ctx.send("I can't pause when nothing is playing in the first place!")
        except:
            return


    @commands.command(name='stop')
    async def stop(self, ctx: commands.Context):
        """
        Rudely kick me out of the voice channel. It's alright, I won't get mad... Just watch out when you go to sleep.
        This is the preferred way of disconnecting me. PLEASE DON'T MANUALLY DISCONNECT ME I WILL LITERALLY FIND YOU AND END YOU.
        You'll genuinely break the music system for a good 5 mins if you manually disconnect me. So don't.

        Usage: 
        `.stop` to end the music streaming session.
        """
        try:
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.message.guild)
            if voice:
                voice = await voice.disconnect()
                voice.cleanup()
                self.clean_queue(True)
            else:
                return await ctx.send("There's nothing to stop when I'm not in a voice channel!")
        except:
            return
        
    @commands.command(name='clear')
    async def clear(self, ctx:commands.Context):
        """
        Clear the music queue in case you added a bunch of junk you didn't wanna add, or you just want to be annoying.

        Usage: 
        `.clear` to clear the queue.
        """
        self.clean_queue(False)
        return await ctx.send("Queue cleared.")

    @commands.command(name='skip')
    async def skip(self, ctx: commands.Context):
        """
        Skip the current song. A classic.

        Usage: 
        `.skip` to skip.
        """
        try:
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.message.guild)
            if voice and (voice.is_playing() or voice.is_paused()):
                await ctx.send("current song skipped")
                await voice.stop()
                
            else:
                return await ctx.send("There's nothing to skip.")
        except:
            return

    @commands.command(name='loop', aliases=['repeat'])
    async def loop(self, ctx: commands.Context, mode: str = ''):
        """
        Loop the current song or the whole queue or loop nothing at all!
        It's pretty lenient in its input requirements so I can't wait to see how you break this one.

        Usage: 
        `.loop [mode]` to switch to mode
        `.loop` to toggle between off and loop current

        Modes: 
        loop off: 'off', '0'
        loop current: 'one','current', '1'
        loop queue: 'queue', 'all', 'everything', 'on', '2'
        """
        if self._loop == 2:
            self.lqueue.pop()
        # Toggles between looping the current track and not looping anything when no input is given
        if not mode and self._loop:
            self._loop = 0
            return await ctx.send("Loop turned Off")
        if not mode and not self._loop:
            self._loop = 1
            return await ctx.send("Will loop the current song.")
        
        # toggles between the different loop modes depending on the input given
        if mode.lower() not in ['queue', 'one', 'current', 'all', 'everything', 'none', 'off', 'on', '0', '1', '2']:
            return await ctx.send("That is not a valid looping mode.")
        if mode.lower() in ['one','current', '1']:
            self._loop = 1
            return await ctx.send("Will loop the current song.")
        if mode.lower() in ['queue', 'all', 'everything', 'on', '2']:
            self._loop = 2
            self.lqueue.append(self.current)
            return await ctx.send("Will loop the queue.")
        self._loop = 0
        return await ctx.send("Loop turned Off")


    @commands.command(name='queue')
    async def view_queue(self, ctx: commands.Context):
        """
        View the currently played song and the whole queue while you're at it.

        Usage: 
        `.queue` to view the queue.
        """
        embed = Embed(title='Music Queue:')
        embed.description = f"**Currently Playing**: [{self.current['title']}](https://youtu.be/{self.current['id']})\n" if self.current else '**Queue is empty**'
        embed.colour = 0xd95270

        if not self.current:
            return await ctx.send(embed=embed)

        total = self.current['duration']

        for num, song in enumerate(self.lqueue[:25]):
            embed.add_field(name='', value=f"{num + 1}. [{song['title']}](https://youtu.be/{song['id']})\n", inline=False)
            total += song['duration']


        footer = f"Total playtime of the queue is {total//3600:02}:{(total%3600)//60:02}:{(total%3600)%60:02}\n"
        footer += f"Looping "
        footer += "is off." if self._loop == 0 else "the current song." if self._loop == 1 else "the queue."

        embed.set_footer(text=footer)

        await ctx.send(embed=embed)


    @commands.command(name='remove')
    async def remove(self, ctx: commands.Context, index:int = None):
        """
        Remove a song at a specified positon from the queue.

        Usage: 
        `.remove [position]` to remove.
        """
        if not index or index > len(self.lqueue) or index < 1:
            return await ctx.send("How can I remove what doesn't exist.")
        self.lqueue.pop(index - 1)
        return await ctx.send(f"Removed #{index} from music queue.")


    async def queue_next_song(self, ctx: commands.Context, search: str):
        """
        Gets the song info from youtube including the url needed to play it and queues it
        """
        try:
            with YoutubeDL(self.dl_opts) as ydl:
                    self.lqueue.append(ydl.extract_info(f'ytsearch:{search}', download=False)['entries'][0])
                    await ctx.send(embed=self.make_music_embed(0, self.lqueue[-1], ctx.message.author.mention))
        except Exception:
            await ctx.send("It seems like youtube is being a piece... \nTry again later or tell <@247071316686012416> to stop being useless and do something about it. smh.")
        


    async def play_next_song(self, ctx: commands.Context, voice: discord.VoiceClient):
        
        await self.queue.join()

        if self._loop == 2:
            self.lqueue.append(self.current)

        while len(self.lqueue) == 0 and not self._loop:
            await sleep(0)

        if not self._loop == 1:
            self.current = {}
            await self.queue.put(self.lqueue.pop(0))
        else:
            await self.queue.put(self.current)

        self.current = await self.queue.get()

        voice.play(discord.FFmpegOpusAudio(self.current['url'],
                                           **self.ffmpeg_opts), after=lambda e: self.queue.task_done())
        await ctx.send(embed=self.make_music_embed(1, self.current, ctx.message.author.mention))

        

        if not voice.is_connected():
            return self.clean_queue(True)
        
        await sleep(1)
        await self.play_next_song(ctx, voice)



    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if member.id == self.bot.user.id and after.channel is None:
            try:
                voice = await discord.utils.get(self.bot.voice_clients, guild=member.guild).disconnect()
                self.clean_queue(True)
                return voice.cleanup()
            except AttributeError:
                return
        else:
            try:
                voice = discord.utils.get(self.bot.voice_clients, guild=member.guild)
                if len(voice.channel.members) == 1:
                    await voice.disconnect()
                    self.clean_queue(True)
                    return voice.cleanup()
            except AttributeError:
                return

    def make_music_embed(self, type: int, song: dict, requester: str):
        embed = Embed()

        if type:
            embed.title = "Currently Playing:"
            embed.colour = 0xfd4aa0
            embed.add_field(name='',value=f"Requested by: {requester}")
        else:
            embed.title = "Queued:"
            embed.colour = 0xf5034b
            embed.add_field(name='',value=f"In position #{len(self.lqueue)}")
        
        embed.description = f"[{song['title']}](https://youtu.be/{song['id']})\n[{song['duration']//60}:{song['duration']%60:02}]"
        embed.set_thumbnail(url=song['thumbnail'])
    
        return embed
    
    def clean_queue(self, curr_too: bool):
        self._loop = 0
        if curr_too:
            self.current = {}
        self.lqueue = []
        try: 
            while self.queue.get_nowait():
                continue
        except Exception:
            return


def setup(bot):
    bot.add_cog(MusicCog(bot))