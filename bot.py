#imports to load variables, access them, use discord API, and use random
import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands

#loading environment variables from local .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#creating a bot with the given command prefix (required to interact with it)
bot = commands.Bot(command_prefix = '!')

#linking event to this bot
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

#command decorator used instead to designate the use of the command with prefix
@bot.command(name = 'random', help = 'Says the author of the context said a random int from 0-10 inclusive')
async def rand_name(ctx):
    #at least one argument is required (ctx = context of the call [ie guild/channel called from])
    await ctx.send(f'User {ctx.author.name} said {random.randint(0, 10)}')

#Converter allows declaration of types given to command (by default all are strings)
@bot.command(name = 'roll', help = 'rolls a dice with n sides')
async def roll_dice(ctx, num_sides: int):
    if (num_sides <= 0):
        await ctx.send('Invalid number of sides!')
    else:
        await ctx.send(f'Rolled a {random.randint(1, num_sides)}')

@bot.command(name = 'create-channel', help = 'creates new messaging channel (optional name can be given)')
@commands.has_role('Admin') #name of role, ensures user issuing this command can do such an action
async def make_channel(ctx, channel_name = 'New channel'):
    guild = ctx.guild
    #converting given channel name to be Discord-safe
    channel_name = channel_name.replace(' ', '-').lower()
    chan = discord.utils.get(guild.channels, name=channel_name)
    #if not already made, make it
    if not chan:
        print(f'Making channel {channel_name}\n')
        await guild.create_text_channel(channel_name)

#called if a user fails a role check
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Invalid permissions for this command')
    else:
        #logs error to local log
        with open('error.log', 'a') as file:
            file.write(f'Error message: {error}\n')

bot.run(TOKEN)