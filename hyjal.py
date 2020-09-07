import re
import json
import time
import urllib.request
import urllib.parse

from player import Player
from blizzard import Blizzard
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from googleapiclient import discovery

blizzard = Blizzard()
# game_date = Game()

all_characters = []

def gen_player():
    key = None
    rl = False
    main = False
    with open('character_list', 'r') as f:
        for i in f:
            line = i.lower().strip().split(' ')
            if line[0] == "#":
                main = True
                key = line[1]
                if len(line) == 3:
                    rl = True
            else:
                if main:
                    main = False
                    name = urllib.parse.quote(line[0])
                    server = line[1]
                    print("Working on " + line[0] + " player object:")
                    print("getting player info")
                    player_info = blizzard.player_profile(name, server)
                    print("getting gear info")
                    gear_info = blizzard.player_gear(name, server)
                    print("getting profession info")
                    profession_info = blizzard.profession_player(name, server)
                    print("getting pvp 2s info")
                    pvp_2s = blizzard.player_pvp(name, server, "2v2")
                    print("getting pvp 3s info")
                    pvp_3s = blizzard.player_pvp(name, server, "3v3")
                    print("getting image url")
                    image_url = blizzard.image_render(name, server)

                    all_characters.append(Player(main, rl, player_info, gear_info, profession_info, pvp_2s, pvp_3s, image_url, key))

                    if rl:
                        rl = False

def gen_gear_table_html():
    print("Creating Gear table")
    gear = [
    "HEAD",
    "NECK",
    "SHOULDER",
    "CHEST",
    "WAIST",
    "LEGS",
    "FEET",
    "WRIST",
    "HANDS",
    "FINGER_1",
    "FINGER_2",
    "TRINKET_1",
    "TRINKET_2",
    "BACK",
    "MAIN_HAND",
    "OFF_HAND"
    ]

    with open('gear_table.html', 'w') as f:
        f.write(  
        "<table style=\"background-color:#000000;color:black;\">\n"
            "<th style=\"background-color:gray\">Name</th>\n"
            "<th style=\"background-color:gray\">Head</th>\n"
            "<th style=\"background-color:gray\">Neck</th>\n"
            "<th style=\"background-color:gray\">Shoulder</th>\n"
            "<th style=\"background-color:gray\">Chest</th>\n"
            "<th style=\"background-color:gray\">Waist</th>\n"
            "<th style=\"background-color:gray\">Legs</th>\n"
            "<th style=\"background-color:gray\">Feet</th>\n"
            "<th style=\"background-color:gray\">Wrist</th>\n"
            "<th style=\"background-color:gray\">Hands</th>\n"
            "<th style=\"background-color:gray\">Ring</th>\n"
            "<th style=\"background-color:gray\">Ring</th>\n"
            "<th style=\"background-color:gray\">Trinket</th>\n"
            "<th style=\"background-color:gray\">Trinket</th>\n"
            "<th style=\"background-color:gray\">Back</th>\n"
            "<th style=\"background-color:gray\">Main Hand</th>\n"
            "<th style=\"background-color:gray\">Off Hand</th>\n"
        )
        for c in all_characters:
            name = c.player_name
            color = c.class_color
            f.write("<tr>\n")
            f.write("   <td style=\"background-color:" + color + "\">" + name + "</td>\n")
            for g in c.gear_list:
                for item in gear:
                    found = False
                    if item == g[0]:
                        f.write("      <td style=\"background-color:" + str(g[2]) + "; text-align:center\">" + str(g[4]) + "</td>\n")
                        found = True
            if not found:
                f.write("      <td></td>\n")
            f.write("</tr>\n")
        f.write("</table>")


def gen_gear_table_sheets():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('cred/hvfd_cred.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('HVFD').sheet1
    hvfd = sheet.get_all_records()
    pprint(hvfd)


gen_player()
for p in all_characters:
    p.download_image(p.bust)
    p.create_image("img/" + p.player_name + ".jpg")
    print(p.player_name)
