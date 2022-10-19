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


with open('copypastas.csv', mode='r', encoding="utf8") as infile:
    reader = csv.reader(infile)
    copypastaDict = {rows[0]:rows[1] for rows in reader}


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


client.run(TOKEN)