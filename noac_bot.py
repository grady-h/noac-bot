import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

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

bot.run(os.getenv('TOKEN'))
