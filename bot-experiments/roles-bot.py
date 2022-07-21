import discord 

"""
client = discord.Client()

@client.event 
async def on_ready():
    print('Bot is now online and ready to roll.')

client.run('OTk4NjE3MzI0ODg0MDg2OTU0.GdXAT1.vBZoSlwbY1kF9bFMni6MWcmdFbNbqUyMaVnQaE')
"""

class MyClient(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_message_id = 999096060079247484


    async def on_ready(self):
        print('Bot is now online and ready to roll.')

    async def on_raw_reaction_add(self, payload):
        """
        Give a role based on a reaction emoji.
        """
        if payload.message_id != self.target_message_id:
            return
        
        guild = client.get_guild(payload.guild_id)

        if payload.emoji.name == '🤦‍♂️':
            role = discord.utils.get(guild.roles, name='facepalm')
            await payload.member.add_roles(role)
        elif payload.emoji.name == '😭':
            role = discord.utils.get(guild.roles, name='cry emoji')
            await payload.member.add_roles(role)
        elif payload.emoji.name == '🤣':
            role = discord.utils.get(guild.roles, name='lol emoj')
            await payload.member.add_roles(role)

    async def on_raw_reaction_remove(self, payload):
        """
        Remove a role based on a reaction-removal emoji.
        """
        if payload.message_id != self.target_message_id:
            return
        
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if payload.emoji.name == '🤦‍♂️':
            role = discord.utils.get(guild.roles, name='facepalm')
            await member.remove_roles(role)
        elif payload.emoji.name == '😭':
            role = discord.utils.get(guild.roles, name='cry emoji')
            await member.remove_roles(role)
        elif payload.emoji.name == '🤣':
            role = discord.utils.get(guild.roles, name='lol emoj')
            await member.remove_roles(role)



intents = discord.Intents.default()
intents.members = True 

client = MyClient(intents=intents)
client.run('OTk4NjE3MzI0ODg0MDg2OTU0.GdXAT1.vBZoSlwbY1kF9bFMni6MWcmdFbNbqUyMaVnQaE')
