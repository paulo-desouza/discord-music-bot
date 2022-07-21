from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command()
async def double_punch(ctx, arg1, arg2):
    """
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
async def info(ctx):
    """
    ctx - context object (information about how the command was executed)
    
    !info
    """

    await ctx.send(ctx.guild)
    await ctx.send(ctx.author)
    await ctx.send(ctx.message.id)




bot.run('OTk4NjE3MzI0ODg0MDg2OTU0.GdXAT1.vBZoSlwbY1kF9bFMni6MWcmdFbNbqUyMaVnQaE')