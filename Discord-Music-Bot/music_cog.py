import discord
from discord.ext import commands
from more_itertools import value_chain

from youtube_dl import YoutubeDL

bot = commands.Bot(command_prefix = '!')

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Keeping track of time until the selected song comes into play.
        self.current_track_duration = 0
        self.timetillplayed = 0

        # Keeping track of the bot's state.
        self.hasnt_played_yet = True            
        self.is_playing = False
        self.is_paused = False
        
        # Music Queue and Queue History (for replay)
        self.replay_queue = []
        self.music_queue = []
        
        # YDL & FFMPEG Options
        self.YDL_OPTIONS = {'format': 'worstaudio', 'noplaylist': 'False'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options':'-vn'}

        # Storing voice channel & client info
        self.voice = None
        self.voice_client = None

    def search_yt(self, item):
        """
        Searches YouTube if given a query (example: lofi hiphop), or fetches the given link to the YouTube video. 
        """

        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                if 'https' in item[0:5]:        
                    info = ydl.extract_info(item, download=False)['entries'][0]
                else:
                    query = " ".join(item)
                    info = ydl.extract_info("ytsearch:%s" % query, download=False)['entries'][0]

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
        """
        Converts time from seconds to hours, minutes and seconds. 
        """
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
        """
        Plays next song in the queue, and keeps looping this function until there is no more songs queued.
        """
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            self.current_track_duration = self.music_queue[0][0]['duration']
            self.music_queue.pop(0)
            
            self.voice_client.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next() )
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        """
        Joins a voice channel, and starts the play_next() loop.
        """
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            if self.voice_client == None:
                self.voice_client = await self.voice.connect()
                self.voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

                if self.voice_client == None:
                    embed = discord.Embed(
                            description='Please join a voice channel before calling me.',
                            colour=discord.Colour.dark_red()
                        )

                    await ctx.send(embed=embed)
                    return
                else:
                    await self.voice_client.move_to(self.voice)
                
                # Pops the song from the queue, and starts playing it. 
                self.music_queue.pop(0)
                self.voice_client.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())

        else:
            self.is_playing = False

    @bot.command(name="play", aliases = ['p','P', "PLAY", 'bora la meu rei', 'BORA LA MEU REI'])
    async def play(self, ctx, *args):
        """
        Plays or adds selected music/playlist to the queue.
        syntax:  !play [music name or playlist URL] 

        """
        query = args
    
        if ctx.author.voice.channel is None:
            embed = discord.Embed(
                            description='Please join a voice channel before calling me.',
                            colour=discord.Colour.dark_red()
                        )

            await ctx.send(embed=embed)
        elif self.is_paused:
            self.voice_client.resume()
        else:
            # Store current channel information.
            voice_channel = ctx.message.author.voice.channel
            self.voice = discord.utils.get(ctx.guild.voice_channels, name=voice_channel.name)

            # Searches for song.
            song = self.search_yt(query)

            # Check if there are any format errors (example: first result is a livestream)
            if type(song) == type(True):
               
                embed = discord.Embed(
                            description='Could not download the song. Please try again. . .',
                            colour=discord.Colour.dark_red()
                        )
                await ctx.send(embed=embed)
            else:
                # Check if its the first song being played. Different messages will be displayed accordingly.
                if self.hasnt_played_yet == False:
                    # Add songs to queue before anything else, since the bot is already playing something 
                    self.music_queue.append([song])
                    self.replay_queue.append([song])
                
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
        
                    # Calculating how much time until playing the queued song.
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

                    # Add songs to playlist and history queues.
                    self.music_queue.append([song])
                    self.replay_queue.append([song])
                    self.current_track_duration = song['duration']
                    self.hasnt_played_yet = False
                    await self.play_music(ctx)

    @bot.command(name='pause', aliases = ['PAUSE', 'stop', 'STOP', 'parar', 'PARAR', 'pare', 'PARE'])
    async def pause(self, ctx):
        """
        Pauses current track.
        !pause
        """

        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.voice_client.pause()
            embed = discord.Embed(
                description = f"{ctx.author} has paused the current track.",
                colour = discord.Colour.dark_red()
            )
            await ctx.send(embed = embed)
        elif self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.voice_client.resume()
            embed = discord.Embed(
                description = f"{ctx.author} has resumed the current track.",
                colour = discord.Colour.dark_red()
            )
            await ctx.send(embed = embed)

    @bot.command(name='resume', aliases = ['r', 'R', 'RESUME'])
    async def resume(self, ctx):
        """
        Resumes current track if paused.
        !resume
        """
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            await self.voice_client.resume()
            embed = discord.Embed(
                description = f"{ctx.author} has resumed the current track.",
                colour = discord.Colour.dark_red()
            )
            await ctx.send(embed = embed)

    @bot.command(name='skip', aliases = ['SKIP', 's', 'S', 'pular','PULAR', 'proxima', 'PROXIMA'])
    async def skip(self, ctx):
        """
        Skips current track.
        !skip
        """
        if self.voice_client != None:
            if len(self.music_queue) == 0:
                self.voice_client.stop()
                embed = discord.Embed(
                description = f'No more songs in queue!',
                colour = discord.Colour.dark_red()
                )
                await ctx.send(embed = embed)
                await self.leave(ctx)
            else:
                embed = discord.Embed(
                description = f'Skipping current song for you.',
                colour = discord.Colour.dark_red()
                )
                await ctx.send(embed = embed)
                self.voice_client.stop()
                await self.play_music(ctx)

    @bot.command(name='queue', aliases = ['q', 'fila', 'FILA', 'Q'])
    async def queue(self, ctx):   
        """
        Displays the current queue.
        !queue
        """
        retval = ''
        for i in range(0, len(self.music_queue)):
            if i > 10: break
            retval += f"Track {i+1}: {self.music_queue[i][0]['title']} \n"

        if retval != "":
            embed = discord.Embed(
                title = 'Queue',
                description = retval,
                colour = discord.Colour.dark_red()
                )
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                description = f'No songs in queue.',
                colour = discord.Colour.dark_red()
                )
            await ctx.send(embed = embed)

    @bot.command(name='history', aliases = ['h', 'historico', 'HISTORY', 'H'])
    async def history(self, ctx):   
        """
        Displays the current replay queue.
        !queue
        """
        retval = ''

        for i in range(0, len(self.replay_queue)):
            retval += f"Track {i+1}: {self.replay_queue[i][0]['title']} \n"
        
        if retval != "":
            embed = discord.Embed(
                title = 'History',
                description = retval,
                colour = discord.Colour.dark_red()
                )
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                description = f'No songs have been played yet.',
                colour = discord.Colour.dark_red()
                )
            await ctx.send(embed = embed)

    @bot.command(name='clear', aliases = ['limpa', 'CLEAR', 'C', 'LIMPA'])
    async def clear(self, ctx):
        """
        Clears up the queue.
        !clear
        """
        self.music_queue = []
        embed = discord.Embed(
                description = f'Queue has been cleared!',
                colour = discord.Colour.dark_red()
                )
        await ctx.send(embed = embed)

    @bot.command(name='leave', aliases=['l','L','VAZA','vaza'])
    async def leave(self, ctx):
        """
        Tells Cheery MC to leave the voice chat. 
        Resets ALL variables except HISTORY(replay_queue) in case it comes back.
        !leave
        """
        self.is_playing = False
        self.is_paused = False
        self.hasnt_played_yet = True

        self.voice = None

        self.music_queue = []
        self.current_track_duration = 0
        self.timetillplayed = 0

        embed = discord.Embed(
                description = f'Bye-bye, until next time! :*',
                colour = discord.Colour.dark_red()
        )
        await ctx.send(embed = embed)
        self.voice_client.stop()
        await self.voice_client.disconnect()
        self.voice_client = None

    @bot.command()
    async def replay(self, ctx, arg):
        """
        Replays any number of the past played tracks. 
        !replay [number of tracks]
        """
        choice = int(arg)
        if len(self.replay_queue) >= choice:
            original_rq_len = len(self.replay_queue)
            embed = discord.Embed(
                    title = f"{ctx.author} has re-queued the listed tracks.",
                    colour = discord.Colour.dark_red()
                )
            while True:
                self.music_queue.append(self.replay_queue[choice-1])
                self.replay_queue.append(self.replay_queue[choice-1])
                embed.add_field(
                    name= f'Song {choice}',
                    value =f'{self.replay_queue[choice-1][0]["title"]}',
                    inline= False
                )
                choice += 1
                if choice > original_rq_len:
                    break
            await ctx.send(embed = embed)
        else:
            embed2 = discord.Embed(
                    title = f"There are less then {arg} tracks in the History queue. Try Again!",
                    colour = discord.Colour.dark_red()
                )
            await ctx.send(embed2=embed2)
