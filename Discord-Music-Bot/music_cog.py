import discord
from discord.ext import commands
from more_itertools import value_chain

from youtube_dl import YoutubeDL

bot = commands.Bot(command_prefix = '!')

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.current_track_duration = 0
        self.hasnt_played_yet = True            
        self.is_playing = False
        self.is_paused = False
        self.track_exists = False

        self.replay_queue = []
        self.music_queue = []
        self.timetillplayed = 0
        self.YDL_OPTIONS = {'format': 'worstaudio', 'noplaylist': 'False'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options':'-vn'}

        self.vc = None


    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False
        return {
            'source': info['formats'][0]['url'], 
            'title': info['title'], 
            'webpage_url': info['webpage_url'],
            'thumbnail': info['thumbnail'], 
            'duration': info['duration'],

            }
    def convert_time(self, seconds):
        minutes = 0
        hours = 0

        while seconds > 60:
            seconds -= 60
            minutes += 1
        while minutes > 60:
            minutes -= 60
            hours += 1
        
        if hours == 0:
            return f"{minutes}:{seconds}" 
        else:
            return f"{hours}:{minutes}:{seconds}"


    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            

            m_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)
            self.current_track_duration = self.music_queue[0][0]['duration']
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False
            self.track_exists = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    embed = discord.Embed(
                            description='Please join a voice channel before calling me.',
                            colour=discord.Colour.dark_red()
                        )

                    await ctx.send(embed=embed)
                    return
                else:
                    await self.vc.move_to(self.music_queue[0][1])
                
                
                self.music_queue.pop(0)
                

                self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())

        else:
            self.is_playing = False
            self.track_exists = False

    
    @bot.command(name="play", aliases = ['p','vai'])
    async def play(self, ctx, *args):
        """
        Plays or adds selected music/playlist to the queue.
        syntax:  !play [music name or playlist URL] 

        """
        query = " ".join(args)
        self.track_exists = True
        if ctx.author.voice is None:
            embed = discord.Embed(
                            description='Please join a voice channel before calling me.',
                            colour=discord.Colour.dark_red()
                        )

            await ctx.send(embed=embed)
        elif self.is_paused:
            self.vc.resume()
        else:
            voice_channel = ctx.author.voice.channel
            song = self.search_yt(query)
            if type(song) == type(True):
                embed = discord.Embed(
                            description='Could not download the song. Please try again. . .',
                            colour=discord.Colour.dark_red()
                        )

                await ctx.send(embed=embed)
            else:
                if self.hasnt_played_yet == False:
                    self.music_queue.append([song, voice_channel])
                    self.replay_queue.append([song, voice_channel])

                    embed = discord.Embed(
                                title = "New song on the queue!",
                                colour=discord.Colour.dark_red()
                            )
                    thumb = song["thumbnail"]
                    
                    embed.set_thumbnail(url=thumb)
                    embed.add_field(
                        name = 'Track',
                        value = f"[{song['title']}]({song['webpage_url']})",
                        inline = False
                    )
                    
                    
                    
                    embed.add_field(
                        name = 'Track Duration',
                        value = self.convert_time(int(song['duration'])),
                        inline = True
                    )
                    
                    totalseconds = 0
                    for i, music in enumerate(self.music_queue):
                        if i > 0:
                            totalseconds += int(self.music_queue[i][0]['duration'])

                    totalseconds += self.current_track_duration
                    self.timetillplayed = totalseconds

                    embed.add_field(
                        name = 'Estimated time until played',
                        value = self.convert_time(self.timetillplayed),
                        inline = True
                    )

                    embed.add_field(
                        name = 'Position in queue:',
                        value = len(self.music_queue),
                        inline = True
                    )
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title = 'A wild song has appeared!',
                        description = f"[{song['title']}]({song['webpage_url']})",
                        colour = discord.Colour.dark_red()
                    )
                    
                    thumb = song["thumbnail"]
                    embed.set_thumbnail(url=thumb)
                    embed.add_field(
                        name = 'Track Duration',
                        value = self.convert_time(int(song['duration'])),
                        inline = True
                    )

                    await ctx.send(embed=embed)

                    self.music_queue.append([song, voice_channel])
                    self.replay_queue.append([song, voice_channel])
                    self.current_track_duration = song['duration']
                    self.hasnt_played_yet = False
                    await self.play_music(ctx)

    
    @bot.command(name='pause')
    async def pause(self, ctx):
        """
        Pauses current track.
        !pause
        """
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            await ctx.send(f"{ctx.author} has paused the current track.")
        elif self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()
            await ctx.send(f"{ctx.author} has resumed the current track.")

    @bot.command(name='resume')
    async def resume(self, ctx):
        """
        Resumes current track if paused.
        !resume
        """
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()
            await ctx.send(f"{ctx.author} has resumed the current track.")

    @bot.command()
    async def skip(self, ctx):
        """
        Skips current track.
        !skip
        """
        if self.vc != None:
            if len(self.music_queue) == 0:
                self.vc.stop()
                await self.play_music(ctx)
                await ctx.send('No more songs in queue! Bye-bye, until next time! :*')
                await self.vc.disconnect()
            else:
                self.vc.stop()
                await self.play_music(ctx)


    @bot.command(name='queue', aliases = ['q', 'fila'])
    async def queue(self, ctx):   
        """
        Displays the current queue.
        !queue
        """

        retval = ''

        for i in range(0, len(self.music_queue)):
            if i > 10: break
            retval += f"{i+1}:{self.music_queue[i][0]['title']} \n"
        
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue.")

    @bot.command(name='history', aliases = ['h', 'historico'])
    async def history(self, ctx):   
        """
        Displays the current replay queue.
        !queue
        """

        retval = ''

        for i in range(0, len(self.replay_queue)):
            retval += f"{i+1}:{self.replay_queue[i][0]['title']} \n"
        
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue.")

    @bot.command(name='clear')
    async def clear(self, ctx):
        """
        Clears up the queue.
        !clear
        """
        self.music_queue = []
        await ctx.send("Music queue cleared.")

    @bot.command(name='leave', aliases=['l', 'vaza'])
    async def leave(self, ctx):
        """
        Tells Cheery MC to leave the voice chat. 
        !leave
        """
        self.is_playing = False
        self.is_paused = False
        await ctx.send('Bye-bye, until next time! :*')
        await self.vc.disconnect()

    @bot.command()
    async def replay(self, ctx, arg):
        """
        Replays any number of the past played tracks. 
        !replay [number of tracks]
        """
        choice = int(arg)
        if len(self.replay_queue) >= choice:
            original_rq_len = len(self.replay_queue)
            while True:
                self.music_queue.append(self.replay_queue[choice-1])
                self.replay_queue.append(self.replay_queue[choice-1])
                await ctx.send(f'{self.replay_queue[choice-1][0]["title"]}') 
                choice += 1
                if choice > original_rq_len:
                    break

            await ctx.send(f"{ctx.author} has re-queued the listed tracks.")
        else:
            await ctx.send(f"There are less then {arg} tracks in the replay queue. Try Again!")
