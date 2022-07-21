import discord

client = discord.Client()

@client.event 
async def on_ready():
    print('Bot is now online and ready to roll.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return 

    if message.content == 'cool':
        await message.add_reaction('\U0001F60E')   # Emoji Reaction. Rad.

@client.event
async def on_reaction_add(reaction, user):                # React to reaction. This method listens for reactions and their users.
    await reaction.message.channel.send(f'{user} reacted with {reaction.emoji}!')


client.run('OTk4NjE3MzI0ODg0MDg2OTU0.GdXAT1.vBZoSlwbY1kF9bFMni6MWcmdFbNbqUyMaVnQaE')