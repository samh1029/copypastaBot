# bot.py
import os
import discord
import io
import random
import csv
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
random.seed()
intents = discord.Intents.all()
client = discord.Client(intents=intents)

copypastaDict = {}

# with io.open("copypastas.txt", encoding="utf8") as f:
#     Lines = f.readlines()
#     for line in Lines:
#         if line.strip():
#             a,b = line.split("$")
#             if "," in a:
#                 copypastaDict[tuple(a.split(","))] = b
#             copypastaDict[a] = b


# with open('copypastas.csv', mode='r') as infile:
#     reader = csv.reader(infile)
#     with open('copypastas.csv', mode='w') as outfile:
#         writer = csv.writer(outfile)
#         copypastaDict = {rows[0]:rows[1] for rows in reader}

copypastaDict = csv.DictReader(open("copypastas.csv"))


@client.event
async def on_ready():
    for guilds in client.guilds:
        print(f'{client.user} has connected to discord server: {guilds}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author.name == "Rainbows__1464" and random.randrange(1,15) == 1:
        await message.channel.send("shutup kyle")
        return
    send = False
    message.content = message.content.lower()
    for key, value in copypastaDict.items():
        if isinstance(key, tuple):
            for i in key:
                if i in message.content:
                    send = True
                    break
        elif key in message.content:
            send = True
        if send:
            await message.channel.send(value)
            break


client.run(TOKEN)