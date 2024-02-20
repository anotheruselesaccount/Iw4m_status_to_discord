
'''
install requirements:
pip install discord.py
pip install colorama
'''

from colorama import init, Fore, Back, Style
from discord.ext import tasks, commands
from datetime import datetime
import platform
import requests
import discord
import ctypes
import json
import os

init(autoreset=True)  # Initialize colorama / enable colors in windows cmd

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

def println(string: str, type: str):
    print(f"{Color.YELLOW}{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}: {Color.RESET}[ {Color.BLUE if type == 'INFO' else Color.RED}{type} {Color.RESET}] {string}")

class Color:
    if platform.system() == 'Windows':
        RED = Fore.RED
        GREEN = Fore.GREEN
        YELLOW = Fore.YELLOW
        BLUE = Fore.BLUE
        CYAN = Fore.CYAN
        RESET = Style.RESET_ALL
        PURPLE = Fore.MAGENTA
    else:
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        RESET = '\033[0m'  # Reset to default color
        PURPLE = '\033[95m'

def get_json_item( item ):
    try:
        with open(os.path.join(os.getcwd(), "config.json"), "r") as json_file:
            data = json.load(json_file)
            return data[item]
    except Exception as e:
        println(f"There was problem while reading json file: {e}.", "ERROR")

token = str(get_json_item('discord_bot_token'))
iw4m_api_url = f"{get_json_item('iw4m_webfront_url')}/api/status"
status_channel = int(get_json_item('discord_channel_id'))
refresh_time = int(get_json_item('refresh_time_in_minutes'))
game = str(get_json_item('game')).upper()
show_players = str(get_json_item('show_players')).lower()

@bot.event
async def on_ready():
    print(f"")
    print(f"        {Color.CYAN}╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮ ")
    print(f"        {Color.CYAN}┃     IW4M api server status bot       ┃ ")
    print(f"        {Color.CYAN}┃     > Created by Unknown Love <      ┃ ")
    print(f"        {Color.CYAN}╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯ ")
    print(f"")
    println(f"{Color.GREEN}Bot started in{Color.RESET}: {[guild.name for guild in bot.guilds]}", "INFO")

    @tasks.loop(minutes=refresh_time)
    async def get_servers():
        await check_status()
        
    get_servers.start()

def remove_colour_codes(string):
    result = []
    i = 0
    while i < len(string):
        if string[i] == '^' and i + 1 < len(string) and string[i + 1].isdigit():
            i += 2
        else:
            result.append(string[i])
            i += 1
    return ''.join(result)

async def check_status():
    try:
        response = requests.get(iw4m_api_url)
        iw4m_api_string = json.loads(response.text)

        game_name = []
        isOnline = []
        name = []
        maxPlayers = []
        currentPlayers = []
        map_alias = []
        player_names = []
        total_players = 0
        total_servers = 0
        players = 0
        number = 0

        for server in iw4m_api_string:
            if game != "" and game != "ALL":
                if server['game'] != game:
                    number += 1
                    continue

            isOnline.append(server['isOnline'])
            name.append(server['name'])
            maxPlayers.append(server['maxPlayers'])
            currentPlayers.append(server['currentPlayers'])
            map_alias.append(server['map']['alias'])
            server_players = iw4m_api_string[number]["players"]
            player_names.append("\n".join([f"• {player['name']}" for player in server_players]))
            game_name.append(server['game'] + '\n') #cant add '\n' later inside f string
            total_players += server['maxPlayers']
            players += server['currentPlayers']
            total_servers += 1
            number += 1

        embed = discord.Embed(timestamp=datetime.utcnow(), title=f"**• Server Status • {'Modern Warfare 3' if game == 'IW5' else 'World at War' if game == 'T4' else 'Black ops 1' if game == 'T5' else 'Black ops 2' if game == 'T6' else 'Black ops 3' if game == 'T7' else ''}**", color=2763306)
        
        for i in range(len(isOnline)):
            if i == 25: #max fields limit in embed message
                break

            if "^" in name[i]:
                name[i] = remove_colour_codes(name[i])

            if "_" in map_alias[i]:
                map_alias[i] = map_alias[i].replace('_', ' ')

            embed.add_field(name=f"{':white_check_mark:' if isOnline[i] else ':x:'} {name[i]}", 
                            value = (
                                f"Status: {'Online' if isOnline[i] else 'Offline'}\n"
                                f"{'Game: ' + game_name[i] if game == '' or game == 'ALL' else ''}"
                                f"Map: {map_alias[i]}\n"
                                f"Players: {currentPlayers[i]}/{maxPlayers[i]}\n"
                                f"{ '```' + player_names[i] + '```' if player_names[i] != '' else '' if show_players == 'true' else ''}"
                            ),
                            inline=True)
                            
        embed.set_footer(text=f"• Last Update: {datetime.now().strftime('%m/%d/%Y, %I:%M:%S %p')}")
        
        channel = bot.get_channel(status_channel)
        async for message in channel.history( limit=10 ):
            if message.author == bot.user:
                await message.edit(embed=embed)
                break
        else:
            await channel.send(embed=embed)
        
        activity = discord.Game(name=f"WATCHING {players}/{total_players} PLAYERS ACROSS {total_servers} SERVERS", type=3)
        await bot.change_presence(status=discord.Status.online, activity=activity)

        println(f"Status check notify.", "INFO")

    except Exception as e:
        println(f"There was problem while checking status: {e}.", "ERROR")

bot.run(token)