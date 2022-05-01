# bot.py
import os
import discord
import json
import io
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

copypastaDict = {}

with io.open("copypastas.txt", encoding="utf8") as f:
    Lines = f.readlines()
    for line in Lines:
        if line.strip():
            a,b = line.split("$")
            if "," in a:
                copypastaDict[tuple(a.split(","))] = b
            copypastaDict[a] = b


@client.event
async def on_ready():
    print(f'{client.user} has connected to discord server: {client.guilds[0]}')


@client.event
async def on_message(message):
    if message.author == client.user:
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