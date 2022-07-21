from discord.ext import commands
import discord



bot = commands.Bot(command_prefix='!')
bot.remove_command('help')


@bot.command()
async def double_punch(ctx, arg1, arg2):
    """
    Double Punches 2 users!!!!!!!
    !double_punch Justin Brad
    """

    await ctx.send(f'Double Punched {arg1} and {arg2}!!!!!')


@bot.command()
async def roundhouse_kick(ctx, *args):
    """
    !roundhouse_kick Justin, Brad, Marina, .......
    """
    everyone = ', '.join(args)
    await ctx.send(f'Roundhouse kicked {everyone}!!!!!!!!!!! ABSOLUTE LEGEND')



@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title='Bot Commands',
        description='Welcome to the help section! Here are all the commands for this game.',
        color=discord.Colour.green()
    )

    #embed.set_thumbnail(url='')    | IMAGE ON EMBED
    embed.add_field(
        name='!help',
        value='List all the commands.',
        inline=True
    )
    embed.add_field(
        name='!double_punch',
        value='Punches two users.',
        inline=True
    )
    embed.add_field(
        name='!roundhouse_kick',
        value='Roundhouse kick any number of people.',
        inline=True
    )

    await ctx.send(embed=embed)




bot.run('OTk4NjE3MzI0ODg0MDg2OTU0.GdXAT1.vBZoSlwbY1kF9bFMni6MWcmdFbNbqUyMaVnQaE')