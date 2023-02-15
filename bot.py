# bot.py
import asyncio
import csv
import datetime
import io
import os
import random
import re
import subprocess
import sys

import discord
import requests
from discord.ext import commands

from config import TOKEN, CHANNEL_ID, COPYPASTAS_FILE, BIRTHDAYS_FILE, SHUTUP_FILE, COMMAND_PREFIX, MC_API_URL



intents = discord.Intents.all()
bot = commands.Bot(command_prefix=COMMAND_PREFIX,intents=intents)
copypasta_dict = reset_csv()


def reset_csv():
    try:
        with open(COPYPASTAS_FILE, 'r', encoding='utf8', newline='') as file:
            reader = csv.DictReader(file)
            copypasta_dict = {row[0]:row[1] for row in reader}
        return copypasta_dict
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error opening file: {e}", file=sys.stderr)
        return None
    except csv.Error as e:
        print(f"Error reading CSV file: {e}", file=sys.stderr)
        return None



def read_file(file_path):
    result = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.rstrip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    result[key] = value.strip()
    except (IOError, OSError) as e:
        print(f"Error opening or reading file: {e}", file=sys.stderr)
    return result


@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(f'{bot.user} has connected to Discord server: {guild}')
    try:
        await bot.wait_until_ready()
        bot.loop.create_task(check_birthday())
    except Exception as e:
        print(f"An error occurred in on_ready: {e}", file=sys.stderr)


async def check_birthday():
    await bot.wait_until_ready()
    while not bot.is_closed():
        today = datetime.datetime.now().strftime("%d/%m")
        for birthday, username in read_file(BIRTHDAYS_FILE).items():
            if today == birthday:
                channel = bot.get_channel(CHANNEL_ID)
                years_to_live = random.randrange(1,10)
                await channel.send(f"Happy birthday {username} 🎂🎉🎈 you have {years_to_live} year(s) left alive")
        await asyncio.sleep(86400)


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    message.content = message.content.lower()
    if message.author == bot.user:
        return
    user_name = message.author.name
    try:
        for username, name in read_file(SHUTUP_FILE).items:
            if user_name == username and random.randrange(1, 15) == 1:
                await message.channel.send(f"shutup {name}")
    except Exception as e:
        print(f'Error reading shutup file: {e}', file=sys.stderr)
    for key, value in copypasta_dict.items():
        if "," in key:
            should_send_copypasta = any(substring in message.content for substring in key.split(","))
        else:
            should_send_copypasta = key in message.content
        if should_send_copypasta and random.randrange(1, 3) == 1:
            await message.channel.send(value)
            break


@bot.command(name="reset", help="Re-grab the copypasta details from the CSV")
async def reset(ctx):
    try:
        subprocess.run(["git", "pull"], check=True)
        copypasta_dict = reset_csv()
        await ctx.send("Successfully reset CSV")
    except subprocess.CalledProcessError as e:
        await ctx.send(f"Error resetting CSV: {e}", file=sys.stderr)
    except Exception as e:
        await ctx.send(f"Unexpected error: {e}", file=sys.stderr)
    else:
        return copypasta_dict


@bot.command(name="mc", help="Get current logged in users of a Minecraft server if any")
async def mc(ctx):
    try:
        server_address = ctx.message.content.split(" ")[1]
        if not is_valid_server_address(server_address):
            await ctx.send("Invalid server address")
            return

        link = MC_API_URL + server_address
        response = requests.get(link)
        response.raise_for_status()

        players = response.json().get("players", {})
        if "list" in players:
            users = ", ".join(players["list"])
            await ctx.send(f"Femboys currently are {users} *˚*(ꈍ ω ꈍ).₊̣̇.")
        else:
            await ctx.send("No femboys on the server *:･ﾟ✧(ꈍᴗꈍ)✧･ﾟ:*")
    except requests.exceptions.HTTPError as e:
        await ctx.send(f"Failed to retrieve server information: {e}", file=sys.stderr)
    except (ValueError, KeyError):
        await ctx.send("Failed to parse server information", file=sys.stderr)
    except Exception as e:
        await ctx.send(f"Unexpected error: {e}", file=sys.stderr)


def is_valid_server_address(server_address):
    # Check if the server address matches the format of a valid Minecraft server address
    # (e.g. "mc.example.com:25565" or "123.45.67.89:25565")
    regex = r"^(?:(?:[a-z0-9]|[a-z0-9][a-z0-9\-]*[a-z0-9])\.)+[a-z]{2,}$|(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}$"
    return bool(re.match(regex, server_address))


bot.run(TOKEN)