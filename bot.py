# bot.py
import os
import discord
from discord.ext import commands
import io
import random
import csv
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
random.seed()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='-',intents=intents)
copypastaDict = {}


def resetCSV():
    with open('copypastas.csv', mode='r', encoding="utf8") as infile:
        reader = csv.reader(infile)
        global copypastaDict
        copypastaDict = {rows[0]:rows[1] for rows in reader}


@bot.event
async def on_ready():
    for guilds in bot.guilds:
        print(f'{bot.user} has connected to discord server: {guilds}')


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    message.content = message.content.lower()
    send = False
    if message.author == bot.user:
        return
    if message.author.name == "Rainbows__1464" and random.randrange(1,15) == 1:
        await message.channel.send("shutup kyle")
        return
    for key, value in copypastaDict.items():
        if "," in key:
            for i in key.split(","):
                if i in message.content:
                    send = True
                    break
        elif key in message.content:
            send = True
        if send:
            await message.channel.send(value)
            break


@bot.command(name="reset", help="Re-grab the copypasta details from the CSV")
async def reset(ctx):
    os.system("git reset --hard master")
    resetCSV()
    await ctx.send("Successfully reset CSV")


resetCSV()
bot.run(TOKEN)