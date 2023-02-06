#basic bot script (making a connection with Discord)
import os
import discord
#useful library for dealing with environment variables
from dotenv import load_dotenv

#loads content from .env file in working directory
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intent = discord.Intents.default()
#allow viewing members and sending/receiving message
intent.members = True
intent.messages = True
client = discord.Client(intents=intent)

#decorator
@client.event
#on_ready is called once Discord has handled the connection and the bot is ready
async def on_ready():
    #same functionality as for loop with break in next two lines, but cleaner
    #guild = discord.utils.find(lambda: g: g.name == GUILD, client.guilds)
    #guild = discord.utils.get(client.guilds, name=GUILD)
    print(f'{client.user.name} has connected to Discord!')
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    
    print(f'{client.user} is connected to {guild.name}, ID: {guild.id}')
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_member_join(member):
    #waits until coroutine is completed before continuing execution (like yield)
    await member.create_dm()
    #makes direct message channel and messages user
    await member.dm_channel.send(f'Hi {member.name}, welcome to this server!')

@client.event
async def on_message(message):
    #if author of the message is the same as the bot, don't do anything
    if message.author == client.user:
        return
    
    if message.content.lower() == 'hi':
        await message.channel.send(f'Response from {client.user.name}')
    elif message.content.lower() == 'raise-exception':
        raise discord.DiscordException

@client.event
async def on_error(event, *args, **kwargs):
    #writing error to local logging file from bot
    with open('error.log', 'a') as file:
        if event == 'on_message':
            file.write(f'Error message: {args[0]}\n')
        else:
            raise

client.run(TOKEN)

#could also create class (extending discord.Client) to implement event handler
class CustClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord')
#then client = CustClient()