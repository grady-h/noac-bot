'''
IMPLEMENTATION

Daily History:
- Keep a daily tally of how many messages each person has sent in the server
- If a person goes over a certain daily message threshold, assign Needs To Touch Grass role for a day

- Every night at 12:00am:
    - Reset the message counts
'''

import discord, os
from discord.ext import commands
from dotenv import load_dotenv
from touch_grass_cog import TouchGrass

load_dotenv()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

SERVER_ID = 1096518509145628793
GENERAL_CHANNEL_ID = 1096518509699289242

# event listeners
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to the server!")
    server = bot.get_guild(SERVER_ID)
    general_channel = bot.get_channel(GENERAL_CHANNEL_ID)
    
    # create role
    await server.create_role(name="Needs To Touch Grass", color=discord.Colour.dark_green())
    touch_grass_role = discord.utils.get(server.roles, name="Needs To Touch Grass")

    # add touch grass cog
    await bot.add_cog(TouchGrass(bot, SERVER_ID, general_channel, touch_grass_role))

    print("Finish initializing")


# commands
@bot.command()
async def ping(ctx):
    await ctx.channel.send("pong")

@bot.command()
async def send(ctx, num):
    for i in range(int(num)):
        await ctx.send(f"Placeholder message #{i+1}")


bot.run(os.getenv('TOKEN'))
