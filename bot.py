# bot.py
import csv
import os
import random
import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(override=True)
TOKEN = os.getenv("DISCORD_TOKEN")
COPYPASTAS_FILE = "copypastas.csv"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-", intents=intents)


def read_csv(COPYPASTAS_FILE):
    try:
        with open(COPYPASTAS_FILE, "r", encoding="utf8", newline="") as file:
            reader = csv.reader(file)
            copypasta_dict = {row[0]: row[1] for row in reader}
        return copypasta_dict
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error opening file: {e}", file=sys.stderr)
        return None
    except csv.Error as e:
        print(f"Error reading CSV file: {e}", file=sys.stderr)
        return None


@bot.event
async def on_ready():
    await bot.tree.sync()
    for guild in bot.guilds:
        print(f"{bot.user} has connected to Discord server: {guild}")


@bot.event
async def on_message(message):
    if message.author == bot.user:  # Don't react to your own messages
        return

    message_content = message.content.lower()

    for key, value in copypasta_dict.items():
        if any(substring in message_content for substring in key.split(",")):
            if random.randrange(1, 3) == 1:  # Random chance (1/3) to send
                await message.channel.send(value)
                break  # Stop after sending one copypasta


copypasta_dict = read_csv(COPYPASTAS_FILE)
bot.run(TOKEN)
