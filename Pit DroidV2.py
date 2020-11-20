#Pit Droid.py
import datetime
import asyncio
import discord
import time
from discord.ext import commands
from datetime import timedelta, datetime
from datetime import date

Token = open("token.txt", "r").read()
client = discord.Client()
client = commands.Bot(command_prefix='!')

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
    

@client.event
async def on_ready():
    print(f'{client.user} logged in!')
async def on_message(message):
    # DO NOT RESPOND TO SELF
    if message.author == client.user:
        return

@client.command()
# Stopwatch Prompt - quick and fast, only supports minutes.
async def stopwatch(ctx):
    await ctx.send('*******Stopwatch Service*******\nA quick countdown timer\nUsage: !set_stopwatch minutes Description\nEx. "!set_stopwatch 10m Brush teeth"')

@client.command()
# Set Stopwatch
async def set_stopwatch(ctx, time, description):
    seconds = 0
    if time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    await ctx.send('Setting the stopwatch for:\nTime: ' + counter + '\nDescription: ' + description)
    await asyncio.sleep(seconds)
    await ctx.send('Countdown finished -> ' + description)
    return

@client.command()
# Reminder Prompt - Using date, time, and a description.
async def reminder(ctx):
    await ctx.send('*******Reminder Service*******\nGive a date, time, and description\nUsage: !set_reminder Date Time Description\n Ex. "!set_reminder 2020-02-15 19:20:00 Brush teeth"')

@client.command()
# Set Reminder
async def set_reminder(ctx, date, time, description):
    # Add to List
    reminderObject = Reminder(date, time, description)
    reminderList.append(reminderObject)

    # Find difference in date and time
    await ctx.send('Setting a Reminder....\nDate: ' + date + '\nTime: ' + time + '\nDescription: ' + description)
    currentDate = datetime.now()

    futureDate = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S')
    timedelta = futureDate - currentDate
    totalSeconds = timedelta.days * 24 * 3600 + timedelta.seconds
    await asyncio.sleep(totalSeconds)
    await ctx.send('Here is your reminder -> ' + description)

@client.command()
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
client.run(Token)
