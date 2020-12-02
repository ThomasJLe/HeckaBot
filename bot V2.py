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
async def on_connect():
    ctx.message

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord')

@bot.command(name='hello', brief='The bot says hello back', description='The bot says hello back to the user that sent the command')
async def greeting(ctx):
    response = f'hi {ctx.author.name}'
    await ctx.send(response)

@bot.command(name='join', brief='Make the bot join the call', description='Make the discord bot join the voice channel you are currently in')
async def join(ctx):
    channel = ctx.author.voice.channel
    voice_clients[channel] = await channel.connect()

@bot.command(name='leave', brief='Make the bot leave the call', description='Make the discord bot leave the voice channel you are currently in')
async def leave(ctx):
    voice_clients.pop(ctx.author.voice.channel)
    await ctx.voice_client.disconnect()

@bot.command(name='play', brief='Make the bot play youtube audio', description='Make the bot play any youtube audio with the given link')
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

@bot.command(name='pause', brief='Pause the song', description='Pauses the song that is currently being played by the discord bot')
async def pause(ctx):
    channel = ctx.author.voice.channel
    voice = voice_clients[channel]
    voice.pause()

@bot.command(name='resume', brief='Resumes the song last played', description='Resumes the song where it left off')
async def resume(ctx):
    channel = ctx.author.voice.channel
    voice = voice_clients[channel]
    voice.resume()

@bot.command(name='stop', brief='Stops playing the song', description='Completely stops playing the music')
async def stop(ctx):
    channel = ctx.author.voice.channel
    voice = voice_clients[channel]
    voice.stop()

bot.run(TOKEN)