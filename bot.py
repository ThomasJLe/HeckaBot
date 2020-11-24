#bot.py
import os
import discord
import youtube_dl
from pafy import new
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
ffmpeg_opts = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
voice_clients = {}

queue = {}

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord')

@bot.command(name='hello')
async def greeting(ctx):
    response = f'hi {ctx.author.name}'
    await ctx.send(response)

@bot.command(name='join')
async def join(ctx):
    channel = ctx.author.voice.channel
    voice_clients[channel] = await channel.connect()

@bot.command(name='leave')
async def leave(ctx):
    voice_clients.pop(ctx.author.voice.channel)
    await ctx.voice_client.disconnect()

@bot.command(name='play')
async def play(ctx, *, url):
    channel = ctx.author.voice.channel
    if channel in voice_clients:
        voice = voice_clients[channel]
    else:
        voice_clients[channel] = await channel.connect()
        voice = voice_clients[channel]
    
    await ctx.send(f'**Playing** {url}')
    video = new(url)
    audio = video.getbestaudio().url
    voice.play(FFmpegPCMAudio(audio, **ffmpeg_opts))
    voice.is_playing()

@bot.command(name='vl')
async def vl(ctx):
    print(voice_clients)

@bot.command(name='pause')
async def pause(ctx):
    channel = ctx.author.voice.channel
    voice = voice_clients[channel]
    voice.pause()

@bot.command(name='resume')
async def resume(ctx):
    channel = ctx.author.voice.channel
    voice = voice_clients[channel]
    voice.resume()

@bot.command(name='stop')
async def stop(ctx):
    channel = ctx.author.voice.channel
    voice = voice_clients[channel]
    voice.stop()

bot.run(TOKEN)