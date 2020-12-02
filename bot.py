#bot.py
import os
import discord
import youtube_dl
import datetime
import asyncio
import time
from pafy import new
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
from discord.ext import commands
from datetime import timedelta, datetime, date

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
ffmpeg_opts = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
quotes = ['Apple are nothing but Trumpers.', 'Apple sucks!', 'The best way to get started is to quit talking and begin doing.', 'Don\'t let yesterday take up too much of today.',
        'We generate fears while we sit. We overcome them by action.', 'Whether you think you can or think you can\'t, you\'re right', 'Creativity is intelligence having fun.',
         'You are never too old to set another goal or to dream a new dream.', 'To see what is right and not do it is a lack of courage.', 'Reading is to the mind, as excercise is to the body.']

# Joke Section Global Count/File open
lineCount = 0
jokesFile = open("jokes.txt", "r")

# Shows when the bot is up and running
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord')

# Simple command that says hello back to the user that sent the command
@bot.command(name='hello', brief='The bot says hello back', description='The bot says hello back to the user that sent the command')
async def greeting(ctx):
    response = f'hi {ctx.author.name}'
    await ctx.send(response)

# Makes the bot join the discord call
@bot.command(name='join', brief='Make the bot join the call', description='Make the discord bot join the voice channel you are currently in')
async def join(ctx):
    channel = ctx.author.voice.channel
    voice_clients[channel] = await channel.connect()

# Makes the bot leave the discord call
@bot.command(name='leave', brief='Make the bot leave the call', description='Make the discord bot leave the voice channel you are currently in')
async def leave(ctx):
    voice_clients.pop(ctx.author.voice.channel)
    await ctx.voice_client.disconnect()

# Makes the bot play youtube audio
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

# Used for debugging purposes
@bot.command(name='vl')
async def vl(ctx):
    print(voice_clients)

# Pauses the song
@bot.command(name='pause', brief='Pause the song', description='Pauses the song that is currently being played by the discord bot')
async def pause(ctx):
    channel = ctx.author.voice.channel
    voice = voice_clients[channel]
    voice.pause()

# Resumes the song last played
@bot.command(name='resume', brief='Resumes the song last played', description='Resumes the song where it left off')
async def resume(ctx):
    channel = ctx.author.voice.channel
    voice = voice_clients[channel]
    voice.resume()

# Stops the song that is currently played
@bot.command(name='stop', brief='Stops playing the song', description='Completely stops playing the music')
async def stop(ctx):
    channel = ctx.author.voice.channel
    voice = voice_clients[channel]
    voice.stop()

# Reminder List
reminderList = []
# Reminder Class
class Reminder:
    def __init__(self, date, time, descrption):
        self.date = date
        self.time = time
        self.description = descrption
    def show(self):
        pass

@bot.command(name = 'set_stopwatch', brief = 'A quick countdown timer\nUsage: !set_stopwatch minutes Description', description = 'Example: "!set_stopwatch 10m Brush teeth"')
# Set Stopwatch - only supports minutes and a description
async def set_stopwatch(ctx, time, description):
    seconds = 0
    if time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    await ctx.send('Setting the stopwatch for:\nTime: ' + counter + '\nDescription: ' + description)
    await asyncio.sleep(seconds)
    await ctx.send('Countdown finished -> ' + description)
    return

@bot.command(name='set_reminder', brief = 'Give a date, time, and description\nUsage: !set_reminder Date Time Description', description = 'Ex. "!set_reminder 2020-02-15 19:20:00 Brush teeth"')
# Set Reminder
async def set_reminder(ctx, date, time, description):
    # Add to List
    reminderObject = Reminder(date, time, description)
    reminderList.append(reminderObject)

    # Find difference in date and time
    await ctx.send('Setting a Reminder....\nDate: ' + date + '\nTime: ' + time + '\nDescription: ' + description)
    currentDate = datetime.now()

    # Calculate difference (futureDate - currentDate)
    futureDate = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S')
    timedelta = futureDate - currentDate
    totalSeconds = timedelta.days * 24 * 3600 + timedelta.seconds
    
    # Calculate 1/2 the time for incremental reminder
    halfReminder = timedelta/2
    halfSeconds = halfReminder.days * 24 * 3600 + halfReminder.seconds
    await asyncio.sleep(halfSeconds)
    await ctx.send('You have a reminder coming up soon -> ' + description)

    await asyncio.sleep(halfSeconds)
    await ctx.send('Here is your reminder -> ' + description)

@bot.command(name = 'show_reminders', brief = 'Show all reminders(past/present)', description = 'All reminders that are currently active or have already passed will be displayed.')
# Show reminders
async def show_reminders(ctx):
    count = 1
    for object in reminderList:
        currentDate = datetime.now()
        reminderDate = datetime.strptime(object.date + ' ' + object.time, '%Y-%m-%d %H:%M:%S')
        timedelta = reminderDate - currentDate
        totalSeconds = timedelta.days * 24 * 3600 + timedelta.seconds
        if totalSeconds < 0:
            await ctx.send('Reminder: ' + str(count) + '-> Already Passed\nDate: ' + object.date + '\nTime: ' + object.time + '\nDescription: ' + object.description + '\n')
            count = count + 1
        else:
            await ctx.send('Reminder: ' + str(count) + '-> Active\nDate: ' + object.date + '\nTime: ' + object.time + '\nDescription: ' + object.description + '\n')
            count = count + 1

@bot.command(name='quote', brief='prints a random quote', description='Prints a random inspirational or funny quote')
async def quote(ctx):
    
@bot.command(name = 'joke', brief = 'Returns a terrible joke', description = 'A joke - not guaranteed to be funny')
# Joke Function - reads a line from "jokes.txt" for each "!joke" command. Resets to beginning of file when last line has been reached.
async def joke(ctx):
    global lineCount
    await ctx.send(jokesFile.readline() + '\n')
    if lineCount == 14:
        lineCount = 0
        jokesFile.seek(0)
    else:
        lineCount = lineCount + 1
    

@bot.command(name='quote', aliases=['q', 'Q'], brief='prints a random quote', description='Prints a random inspirational or funny quote')
async def quote(ctx):
    quote = quotes[random.randint(0,9)]
    await ctx.send(quote)
bot.run(TOKEN)
