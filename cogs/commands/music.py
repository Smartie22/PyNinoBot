"""
This module is dedicated for custom commands that can
be set up by the users
Creation Date: 15/01/2023
"""
import discord
from asyncio import Queue, sleep
import logging
# import io
# from regex import match

# from youtube_search import YoutubeSearch
# import ffmpeg
# from pytube import YouTube

# from requests import get
import youtube_dl
from youtube_dl import YoutubeDL

from discord.ext import commands
from discord.embeds import Embed

class Music(commands.Cog):
    """
    This class handles all commands for the music commands
    """
    def __init__(self, bot: commands.Bot):

        logger = logging.getLogger('ydl')
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(filename='ydl.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(handler)

        self.bot = bot
        self.dl_opts = {
                    'format': 'bestaudio/best',
                    'logger': logger
                }
        self.ffmpeg_opts = {
                    'options': '-vn',
                    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                }
        
        self.queue = Queue(1)
        self.current = {}
        self.lqueue = []


    @commands.command(name='play', aliases=['p'])
    async def play(self, ctx: commands.Context, *, search: str =''):
        """
        Play the music you want in your voice chat!
        """
        if not search == '':
            # try:
                # manages the connection to a voice channel the user is in
            vc:discord.VoiceChannel = discord.utils.get(ctx.message.guild.voice_channels, name=ctx.message.author.voice.channel.name)
            voice:discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.message.guild)

            if vc is None:
                return await ctx.send("You're not in a voice channel. Who am I going to play to...")
            
            await self.queue_next_song(ctx, search)

            # if not connected then connect and if connected ensure the connection is to the right vc
            try:
                voice:discord.VoiceClient = await vc.connect()
                await self.play_next_song(ctx, voice)
            except discord.ClientException:
                voice:discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.message.guild)

            if vc != voice.channel:
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
        Pause the music currently playing, if any.
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
        self.clean_queue(False)
        return await ctx.send("Queue cleared.")

    @commands.command(name='skip')
    async def skip(self, ctx):
        try:
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.message.guild)
            if voice and (voice.is_playing() or voice.is_paused()):
                await ctx.send("current song skipped")
                await voice.stop()
                
            else:
                return await ctx.send("There's nothing to skip.")
        except:
            return


    @commands.command(name='queue')
    async def view_queue(self, ctx: commands.Context):
        embed = Embed(title='Music Queue:')
        embed.description = f"**Currently Playing**: [{self.current['title']}](https://youtu.be/{self.current['id']})\n" if self.current else '**Queue is empty**'
        embed.colour = 0xd95270

        if not self.current:
            return await ctx.send(embed=embed)

        total = self.current['duration']

        for num, song in enumerate(self.lqueue[:25]):
            embed.add_field(name='', value=f"{num + 1}. [{song['title']}](https://youtu.be/{song['id']})\n", inline=False)
            total += song['duration']

        embed.set_footer(text=f"Total playtime of the queue is {total//3600:02}:{(total%3600)//60:02}:{(total%3600)%60:02}")

        await ctx.send(embed=embed)


    @commands.command(name='remove')
    async def remove(self, ctx: commands.Context, index:int):
        if index > len(self.lqueue) or index < 1:
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
            await ctx.send("There was an error while finding the track... please try again...")
        


    async def play_next_song(self, ctx: commands.Context, voice: discord.VoiceClient):
        
        await self.queue.join()
        self.current = {}
        while len(self.lqueue) == 0:
            await sleep(0)
            
        await self.queue.put(self.lqueue.pop(0))

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
                return await voice.cleanup()
            except AttributeError:
                return
        else:
            try:
                voice = discord.utils.get(self.bot.voice_clients, guild=member.guild)
                if len(voice.channel.members) == 1:
                    await voice.disconnect()
                    self.clean_queue(True)
                    return await voice.cleanup()
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
        if curr_too:
            self.current = {}
        self.lqueue = []
        try: 
            while self.queue.get_nowait():
                continue
        except Exception:
            return


def setup(bot):
    bot.add_cog(Music(bot))