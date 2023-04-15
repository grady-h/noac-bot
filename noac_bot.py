'''
FEATURE IDEAS

GO TOUCH GRASS
    - Designates the person with the most messages sent as the biggest
      stinky loser of the server
    - Gives "Needs To Touch Grass" and "Really Needs To Touch Grass" role

    Full History:
    - Keep an all-time tally of how many messages each person has sent in the server
    - User with all time high gets assigned a special Really Needs To Touch Grass role

    Weekly History:
    - Keep a weekly tally of how many messages each person has sent in the server
    - If a person goes over a certain weekly message threshold, assign Touch Grass role for a week

    Daily History:
    - Keep a daily tally of how many messages each person has sent in the server
    - If a person goes over a certain daily message threshold, assign Needs To Touch Grass role for a day
'''

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

global SERVER_ID
global server
global GENERAL_CHANNEL_ID
global general_channel
global member_msg_count
global touch_grass  # role
global touch_grass_member  # member
SERVER_ID = 1096518509145628793
GENERAL_CHANNEL_ID = 1096518509699289242
member_msg_count = {}  # {member1: msg_count, member2: msg_count, ...}
touch_grass = None
touch_grass_member = None


# event listeners
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to the server!")
    global server
    global general_channel
    global touch_grass_member
    global touch_grass
    server = bot.get_guild(SERVER_ID)
    general_channel = bot.get_channel(GENERAL_CHANNEL_ID)

    # get all members
    members = []
    for member in bot.get_all_members():
        # exclude bots
        if member.bot:
            continue
        members.append(member)
    # get all channels
    channels = []
    for channel in bot.get_all_channels():
        # exclude non text channels
        if type(channel) != discord.channel.TextChannel:
            continue
        channels.append(channel)

    # count the number of messages each member has
    for member in members:
        msg_count = 0
        for channel in channels:
            async for message in channel.history(limit=20):
                if message.author == member:
                    msg_count += 1
        # store in member message count dictionary
        member_msg_count[member] = msg_count

    # find member with max message count
    touch_grass_member = list(member_msg_count.keys())[0]
    for member in member_msg_count:
        if member_msg_count[member] > member_msg_count[touch_grass_member]:
            touch_grass_member = member
    
    # create role
    await server.create_role(name="Needs To Touch Grass", color=discord.Colour.dark_green())
    touch_grass = discord.utils.get(server.roles, name="Needs To Touch Grass")

    # # assign member with role
    await touch_grass_member.add_roles(touch_grass)

    # send message
    await general_channel.send(f"<@{touch_grass_member.id}> needs to touch grass! They have {member_msg_count[touch_grass_member]} messages sent!")
    
    print("Finish initializing")


@bot.event
async def on_message(message):
    author = message.author
    if author == bot.user:
        return
    if message.content.startswith('/'):
        await bot.process_commands(message)
        return
    
    global general_channel
    global member_msg_count
    global touch_grass
    global touch_grass_member
    
    # increase author's message count
    member_msg_count[author] += 1

    # check if author is already the touch grass member
    if author.get_role(touch_grass.id) != None:
        return

    # check to see if they have more messages than current non grass toucher
    author_count = member_msg_count[author]
    current_max = member_msg_count[touch_grass_member]
    if author_count > current_max:
        # remove role from current max member
        await touch_grass_member.remove_roles(touch_grass)
        # make author new touch grass member
        await author.add_roles(touch_grass)
        touch_grass_member = author
        # send message
        await general_channel.send(f"<@{touch_grass_member.id}> is the new non-grass toucher with {member_msg_count[touch_grass_member]} messages!")


# commands
@bot.command()
async def ping(ctx):
    await ctx.channel.send("pong")

@bot.command()
async def count(ctx):
    count = 0
    async for message in ctx.channel.history(limit=None):
        if message.author == bot.user:
            continue
        count += 1
    await ctx.send(f"There are {count} messages in this channel")

@bot.command()
async def send(ctx, num):
    for i in range(int(num)):
        await ctx.send(f"Placeholder message #{i}")


bot.run(os.getenv('TOKEN'))
