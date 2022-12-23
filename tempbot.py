import csv
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_2')
intents = discord.Intents.all()

# Open the CSV file and read its contents into a list of tuples
with open('copypastas.csv', 'r', encoding="utf8") as file:
    reader = csv.reader(file)
    copypasta_list = list(reader)

# Create a dictionary from the list of tuples, using the first element of each tuple as the key
copypasta_dict = {t[0]: t[1] for t in copypasta_list}

client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    # Check if the message content is a key in the copypasta dictionary
    print(copypasta_dict[message.content]).encode('utf-8')
    if message.content.lower() in copypasta_dict.keys():
        print(copypasta_dict)
        # If it is, send the corresponding copypasta
        await message.channel.send(copypasta_dict[message.content.lower()]).encode('utf-8')

client.run(TOKEN)
