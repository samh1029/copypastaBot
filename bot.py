# bot.py
import os
import subprocess
import discord
from discord.ext import commands
import io
import random
import csv
from dotenv import load_dotenv
import requests
import datetime
import asyncio
import re

intents = discord.Intents.all()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
CSV_FILE = 'copypastas.csv'
BIRTHDAYS_FILE = 'birthdays.txt'
SHUTUP_FILE = 'shutup.txt'
MC_API_URL = 'https://api.mcsrvstat.us/2/'

bot = commands.Bot(command_prefix='-',intents=intents)


def reset_csv():
    with open('copypastas.csv', 'r', encoding='utf8', newline='') as file:
        reader = csv.DictReader(file)
        copypasta_dict = {rows[0]:rows[1] for rows in reader}
    return copypasta_dict


def read_file(file_path):
    with open(file_path, 'r') as file:
        result = {line.split("=")[0]: ' '.join(line.split("=")[1:]) for line in file if line.strip() and not line.startswith('#')}
    return result



@bot.event
async def on_ready():
    for guilds in bot.guilds:
        print(f'{bot.user} has connected to discord server: {guilds}')
    await bot.wait_until_ready()
    bot.loop.create_task(check_birthday())


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
        print(f'Error reading shutup file: {e}')
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
        await ctx.send(f"Error resetting CSV: {e}")
    except Exception as e:
        await ctx.send(f"Unexpected error: {e}")
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
        await ctx.send(f"Failed to retrieve server information: {e}")
    except (ValueError, KeyError):
        await ctx.send("Failed to parse server information")
    except Exception as e:
        await ctx.send(f"Unexpected error: {e}")


def is_valid_server_address(server_address):
    # Check if the server address matches the format of a valid Minecraft server address
    # (e.g. "mc.example.com:25565" or "123.45.67.89:25565")
    regex = r"^(?:(?:[a-z0-9]|[a-z0-9][a-z0-9\-]*[a-z0-9])\.)+[a-z]{2,}$|(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}$"
    return bool(re.match(regex, server_address))


copypasta_dict = reset_csv()
bot.run(TOKEN)