import json
from contextlib import closing
from requests import get
import datetime

#version 2.0

class Player:
    def __init__(self, player_name, date, stats):
        self.player_name = player_name
        self.date = date
        self.stats = stats

def simple_get(url):
    with closing(get(url, stream=True)) as resp:
        return resp.content


def create_entry(username, date):
    url = "http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player=" + username
    stats = str(simple_get(url))
    stats_separated = stats.strip("b'").split('\\n')

    stats_log = {}

    info_list = ['Overall', 'Attack', 'Defence', 'Strength', 'Hitpoints', 'Ranged', 'Prayer', 'Magic',
                 'Cooking', 'Woodcutting','Fletching', 'Fishing', 'Firemaking', 'Crafting', 'Smithing', 'Mining',
                 'Herblore', 'Agility', 'Thieving', 'Slayer', 'Farming', 'Runecraft', 'Hunter', 'Construction']

    parameters_list = ['Rank', 'Level', 'XP']

    for index, entry in enumerate(stats_separated):
        individual_stat_complete = {}
        total_stats_info = entry.split(',')

        for index_2, piece in enumerate(total_stats_info):
            individual_stat_complete[parameters_list[index_2]] = piece

        if index < len(info_list):
            stats_log[info_list[index]] = individual_stat_complete

    return stats_log


def load_list(filename):
    try:
        with open(filename, 'r') as read_file:
            decoded_xp_log = json.load(read_file)
        return decoded_xp_log
    except IOError:
        return {}


def write_list(filename, data={}):
    with open(filename, "w") as write_file:
        json.dump(data, write_file)


def update_list(filename, username, date):
    try:
        master_log = load_list(filename)
        master_log[date] = create_entry(username, date)
        write_list(filename, master_log)
    except:
        print("User doesn't exist")


if __name__ == "__main__":
    username = input("Enter your username: ")
    filename = username + '_log.json'
    date = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")

    #player = Player(username, date, create_entry(username, date))
    update_list(filename, username, date)










