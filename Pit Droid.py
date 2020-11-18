#bot.py
#import os
import asyncio
import discord
from discord.ext import commands

Token = open("token.txt", "r").read()
client = discord.Client()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print(f'{client.user} logged in!')
async def on_message(message):
    # DO NOT RESPOND TO SELF
    if message.author == client.user:
        return

@client.command()
async def reminder(ctx):
    # Reminder prompt
    await ctx.send('*******Reminder Service*******\nSet a reminder.\nUsage: set_reminder minutes Description\n Ex. "set_reminder 10m Brush teeth"')

@client.command()
async def set_reminder(ctx, time, description):
    seconds = 0
    if time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    await ctx.send('Setting a reminder for you:\nTime: ' + counter + '\nDescription: ' + description)
    await asyncio.sleep(seconds)
    await ctx.send('HERES YOUR REMINDER ' + description)
    return




client.run(Token)