import discord 
import os
from discord.ext import commands

token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix = '!')

bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    
    
    await load('music_cog')


@bot.command()
async def load(music_cog):
    try:
        await bot.load_extension(music_cog)
        print('Loaded {}'.format(music_cog))

    except Exception as error:
        print('{} cannot be loaded. [{}]'.format(music_cog, error))


    
@bot.command(name="help")
async def help(ctx):
    """
    Displays available commands. 
    !help
    """
    embed = discord.Embed(
        title = 'Bot Commands',
        description = 'You have found the help section! Here are all the possible Cherry MC actions. ',
        colour = discord.Colour.dark_red()
    )

    embed.set_thumbnail(url='https://archives.bulbagarden.net/media/upload/e/e1/HOME420.png')

    embed.add_field(
        name = '!play',
        value = 'Plays or adds selected music/playlist to the queue. \n syntax:  !play [music name or playlist URL] ',
        inline=False
    )

    embed.add_field(
        name = '!queue',
        value = 'Displays the queue. \n syntax:  !queue',
        inline=False
    )

    embed.add_field(
        name = '!clear',
        value = 'Clears all the tracks from the queue. \n syntax:  !clear ',
        inline=False
    )

    embed.add_field(
        name = '!pause',
        value = 'Pauses current playing track. \nsyntax: !pause',
        inline=False
    )

    embed.add_field(
        name = '!resume',
        value = 'Resumes current paused track. \nsyntax: !resume',
        inline=False
    )

    embed.add_field(
        name = '!skip',
        value = 'Skips current track.\nsyntax: !skip',
        inline=False
    )

    embed.add_field(
        name = '!replay',
        value = 'Requeues any number of previously played tracks. \nsyntax: !replay [track number to start playing from]',
        inline=False
    )

    embed.add_field(
        name = '!history',
        value = 'Displays all the previously AND currently queued tracks. \nsyntax: !history',
        inline=False
    )

    embed.add_field(
        name = '!leave',
        value = 'Kicks the bot out of the voice channel. \n syntax: !leave ',
        inline=False
    )

    await ctx.send(embed=embed)
    





bot.run(token)







