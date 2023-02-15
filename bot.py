# bot.py
import os
import discord
from discord.ext import commands
import io
import random
import csv
from dotenv import load_dotenv
import requests
import datetime
import asyncio

intents = discord.Intents.all()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
CSV_FILE = 'copypastas.csv'
BIRTHDAYS_FILE = 'birthdays.txt'
SHUTUP_FILE = 'shutup.txt'
MC_API_URL = 'https://api.mcsrvstat.us/2/'
BIRTHDAYS_DICT = read_file(BIRTHDAYS_FILE)
USER_DICT = read_file(SHUTUP_FILE)

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
        for birthday, username in BIRTHDAYS_DICT.items():
            if today == birthday:
                channel = bot.get_channel(CHANNEL_ID)
                years_to_live = random.randrange(1,10)
                await channel.send(f"Happy birthday {username} 🎂🎉🎈 you have {years_to_live} year(s) left alive")
        await asyncio.sleep(86400)


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    message.content = message.content.lower()
    send = False
    if message.author == bot.user:
        return
    user_name = message.author.name
    if user_name in USER_DICT and random.randrange(1, 15) == 1:
        await message.channel.send(f"shutup {USER_DICT[user_name]}")
    for key, value in copypasta_dict.items():
        if "," in key:
            send = any(i in message.content for i in key.split(","))
        else:
            send = key in message.content
        if send and random.randrange(1, 3) == 1:
            await message.channel.send(value)
            break


@bot.command(name="reset", help="Re-grab the copypasta details from the CSV")
async def reset(ctx):
    os.system("git pull")
    copypasta_dict = reset_csv()
    await ctx.send("Successfully reset CSV")


@bot.command(name="mc", help="Get current logged in users of a MC server if any")
async def mc(ctx):
    server_address = ctx.message.content.split(" ")[1]
    link = MC_API_URL + server_address
    response = requests.get(link)
    try:
        users = ', '.join(response.json()["players"]["list"])
        await ctx.send(f"Femboys currently are {users} *˚*(ꈍ ω ꈍ).₊̣̇.")
    except:
        await ctx.send("No femboys on the server *:･ﾟ✧(ꈍᴗꈍ)✧･ﾟ:*")


copypasta_dict = reset_csv()
bot.run(TOKEN)