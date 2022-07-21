import discord
from discord.ext import commands

from youtube_dl import YoutubeDL

bot = commands.Bot(command_prefix = '!')

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False
        self.track_exists = False

        self.replay_queue = []
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options':'-vn'}

        self.vc = None


    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

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
                    await ctx.send('Could not connect to the voice channel.')
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
            await ctx.send("Please connect to a voice channel!")
        elif self.is_paused:
            self.vc.resume()
        else:
            voice_channel = ctx.author.voice.channel
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send('Could not download the song. Incorrect format, try a different keyword.')
            else:
                await ctx.send(f"{ctx.author} has queued {song['title']} into the playlist!")
                self.music_queue.append([song, voice_channel])
                self.replay_queue.append([song, voice_channel])

                if self.is_playing == False:
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
