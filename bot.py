# bot.py
import os
import discord
from discord.ext import commands
import io
import random
import csv
from dotenv import load_dotenv
import requests


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
random.seed()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='-',intents=intents)
copypastaDict = {}
userDict = {"Rainbows__1464":"kyle","unix":"max"}


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
    try:
        if userDict[message.author.name] and random.randrange(1,15) == 1:
            await message.channel.send(f"shutup {userDict[message.author.name]}")
    except:
        pass
    for key, value in copypastaDict.items():
        if "," in key:
            for i in key.split(","):
                if i in message.content:
                    send = True
                    break
        if key in message.content:
            send = True
        if send and random.randrange(1,3) == 1:
            await message.channel.send(value)
            break
        elif send:
            break


@bot.command(name="reset", help="Re-grab the copypasta details from the CSV")
async def reset(ctx):
    os.system("git pull")
    resetCSV()
    await ctx.send("Successfully reset CSV")


@bot.command(name="mc", help="Get current logged in users of a MC server if any")
async def mc(ctx):
    server_address = ctx.message.content.split(" ")[1]
    link = "https://api.mcsrvstat.us/2/" + server_address
    response = requests.get(link)
    try:
        users = ', '.join(response.json()["players"]["list"])
        await ctx.send(f"Femboys currently are {users}")
    except:
        await ctx.send("No logged in users")


resetCSV()
bot.run(TOKEN)