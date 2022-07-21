import discord

client = discord.Client()

@client.event 
async def on_ready():
    print('Bot is now online and ready to roll.')

@client.event
async def on_message(message):   # Reaction to a message

    if message.author == client.user:   # Checking if its not the bot's message
        return

    if message.content == 'hello':   # Checking for the content of the message 
        await message.channel.send('Yo')     # Bot's message.

@client.event
async def on_message_edit(before, after):   # Reaction to a message edit. 
    await before.channel.send(      
        f'{before.author} edited a message.\n'
        f'Before: {before.content}\n'       # Snitch!
        f'After: {after.content}'
    )

client.run('OTk4NjE3MzI0ODg0MDg2OTU0.GdXAT1.vBZoSlwbY1kF9bFMni6MWcmdFbNbqUyMaVnQaE')
