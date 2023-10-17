import csv
import sys
import random
import re
import requests

def reset_csv(COPYPASTAS_FILE):
    try:
        with open(COPYPASTAS_FILE, 'r', encoding='utf8', newline='') as file:
            reader = csv.reader(file)
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


def is_valid_server_address(server_address):
    # Check if the server address matches the format of a valid Minecraft server address
    # (e.g. "mc.example.com:25565" or "123.45.67.89:25565")
    regex = r"^(?:(?:[a-z0-9]|[a-z0-9][a-z0-9\-]*[a-z0-9])\.)+[a-z]{2,}$|(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}$"
    return bool(re.match(regex, server_address))


def get_porn():
    list = ["4k", "blowjob", "boobs", "cum", "feet", "hentai", "spank", "gasm", "lesbian", "lewd", "pussy"]
    randomList = random.choice(list)
    resp = requests.get(f"http://api.nekos.fun:8080/api/{randomList}")
    data = resp.json()
    return data["image"]