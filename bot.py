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

from config import TOKEN, CHANNEL_ID, COPYPASTAS_FILE, BIRTHDAYS_FILE, SHUTUP_FILE, COMMAND_PREFIX, MC_API_URL, INSULTS
from functions import reset_csv, read_file, is_valid_server_address, get_porn

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=COMMAND_PREFIX,intents=intents)


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
        for username, name in read_file(SHUTUP_FILE).items():
            if user_name == username and random.randrange(1, 15) == 1:
                insult = random.choice(INSULTS)
                await message.channel.send(f"{insult} {name}")
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


@bot.event
async def on_voice_state_update(member, before, after):
    channel = before.channel or after.channel
    if channel.id == 644295914936074316 and member.id == 105398180107018240: # Insert voice channel ID
        if before.channel is None and after.channel is not None: # Member joins the defined channel
            link = get_porn()
            await member.send(link)


@bot.command(name="reset", help="Re-grab the copypasta details from the CSV")
async def reset(ctx):
    try:
        subprocess.run(["git", "pull"], check=True)
        copypasta_dict = reset_csv(COPYPASTAS_FILE)
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


@bot.command()
async def ask(ctx, *words):
    prompt = " ".join(words)
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=500
        )
        await ctx.send(response.choices[0].text)
    except openai.error.AuthenticationError:
        await ctx.send("Invalid OpenAI API key. Please check your API key and try again.")
    except openai.error.APIError as e:
        await ctx.send(f"OpenAI API error: {str(e)}")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")


copypasta_dict = reset_csv(COPYPASTAS_FILE)
bot.run(TOKEN)