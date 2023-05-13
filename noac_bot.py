import discord, os
from discord.ext import commands
from dotenv import load_dotenv
from touch_grass_cog import TouchGrass

load_dotenv()
# TODO: review intents
intents = discord.Intents.all()
GrassBot = commands.Bot(command_prefix='/', intents=intents)

SERVER_ID = 1096518509145628793
GENERAL_CHANNEL_ID = 1096518509699289242

# event listeners
@GrassBot.event
async def on_ready():
    print(f"{GrassBot.user} has connected to the server!")
    server = GrassBot.get_guild(SERVER_ID)
    general_channel = GrassBot.get_channel(GENERAL_CHANNEL_ID)
    member_msg_count = {}

    # get all channels
    channels = []
    for channel in GrassBot.get_all_channels():
        # exclude non text channels
        if type(channel) != discord.channel.TextChannel:
            continue
        channels.append(channel)

    # count the number of messages each member has sent
    for channel in channels:
        async for message in channel.history(limit=None):
            if message.author.bot:
                continue
            try:
                member_msg_count[message.author] += 1
            except KeyError:
                member_msg_count[message.author] = 1
    
    # find member with max message count
    touch_grass_member = list(member_msg_count.keys())[0]
    for member in member_msg_count:
        if member_msg_count[member] > member_msg_count[touch_grass_member]:
            touch_grass_member = member

    # create role
    # await server.create_role(name="Needs To Touch Grass", color=discord.Colour.dark_green())
    touch_grass_role = discord.utils.get(server.roles, name="Needs To Touch Grass")

    # TODO: send initial message
    # assign member with role
    await touch_grass_member.add_roles(touch_grass_role)

    for member in member_msg_count:
        member_msg_count[member] = 0

    # add touch grass cog
    await GrassBot.add_cog(TouchGrass(GrassBot, general_channel, touch_grass_role, touch_grass_member, member_msg_count))

    print("Finish initializing")

GrassBot.run(os.getenv('TOKEN'))
