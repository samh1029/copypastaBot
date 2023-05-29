import os
from dotenv import load_dotenv

load_dotenv()
# Discord bot token
TOKEN = os.getenv('DISCORD_TOKEN')

OPENAPI = os.getenv('OPENAI_TOKEN')

# Discord channel ID where the bot will post messages
CHANNEL_ID = int(os.getenv('CHANNEL_ID', default=0))

# Path to the CSV file that stores copypastas
COPYPASTAS_FILE = 'copypastas.csv'

# Path to the file that stores birthdays
BIRTHDAYS_FILE = 'birthdays.txt'

# Path to the file that stores shutup messages
SHUTUP_FILE = 'shutup.txt'

# Prefix for bot commands
COMMAND_PREFIX = '-'

# URL to the MC Server Status API
MC_API_URL = 'https://api.mcsrvstat.us/2/'

INSULTS = ("fuck you", "get gud", "youre a cunt", "this guy is a wanker ->")