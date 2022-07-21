import discord 
from discord.ext import commands
import os

from music_cog import music_cog

bot = commands.Bot(command_prefix = '!')
bot.remove_command('help')
bot.add_cog(music_cog(bot))



@bot.command()
async def help(ctx):
    """
    Displays available commands. 
    !help
    """
    embed = discord.Embed(
        title = 'Bot Commands',
        description = 'You have found the help section! Here are all the possible Cheery MC actions. ',
        colour = discord.Colour.dark_red()
    )

    embed.set_thumbnail(url='https://archives.bulbagarden.net/media/upload/e/e1/HOME420.png')

    embed.add_field(
        name = '!play',
        value = 'Plays or adds selected music/playlist to the queue. \n syntax:  !play [music name or playlist URL] ',
        inline=False
    )

    embed.add_field(
        name = '!pause',
        value = 'Pauses current playing track. \nsyntax: !pause',
        inline=False
    )

    embed.add_field(
        name = '!skip',
        value = 'Skips current track.\nsyntax: !pause',
        inline=False
    )

    embed.add_field(
        name = '!replay',
        value = 'Requeues any number of previously played tracks. \nsyntax: !replay [int]',
        inline=False
    )

    await ctx.send(embed=embed)


bot.run('OTk5MzU2Nzc1MTkzMTIwNzk4.GyL-2Q.0W0VbHoRZWMNy8Fgq7Xf0cPuKvPLOhQ1lxu9lE')
