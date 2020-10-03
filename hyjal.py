import re
import json
import time
import urllib.parse

from player import Player
from blizzard import Blizzard

blizzard = Blizzard()

all_characters = []
app_profession = {}


def gen_player():
    all_characters = []
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
                    rl = False
                    main = False
                    name = urllib.parse.quote(line[0])
                    server = line[1]
                    print("Working on " + line[0] + " player object:")
                    print("getting player info")
                    player_info = blizzard.profile_character_profile(name, server)
                    print("getting gear info")
                    gear_info = blizzard.profile_character_equipment(name, server)
                    print("getting profession info")
                    profession_info = blizzard.profile_character_profession(name, server)
                    print("getting pvp 2s info")
                    pvp_2s = blizzard.profile_character_pvp(name, server, "2v2")
                    print("getting pvp 3s info")
                    pvp_3s = blizzard.profile_character_pvp(name, server, "3v3")
                    print("getting image url")
                    image_url = blizzard.profile_character_media(name, server)

                    all_characters.append(Player(main, rl, player_info, gear_info, profession_info, pvp_2s, pvp_3s, image_url, key))


def gen_profession():
    profession_tier = {}
    profession_index = blizzard.game_profession_index()
    for p in profession_index["professions"]:
        current_profession = blizzard.game_profession(p["id"])
        if current_profession["type"]["type"] == "PRIMARY":
            profession_tier[current_profession["name"]] = current_profession["skill_tiers"][0]["name"].split(' / ')[0]
    return profession_tier

    def compair_profession(profession_tier):
        for p in profession_tier:
            print(p)
            tier = profession_tier[p].split(' / ')[0]
            for c in all_characters:
                print(c.profession_list)
                if re.findall(c.profession_list[0][0], p):
                    if c.profession_list[0][3] == tier:
                        print("FOUND_P1")
                if re.findall(c.profession_list[0][0], p):
                    if c.profession_list[0][3] == tier:
                        print("FOUND_P2")

# def mythic_plus():
#     with open('character_list', 'r') as f:
#         index = blizzard.game_mythic_keystone_dungeons_index()
#         current = blizzard.game_mythic_keystone_leaderboard(i["id"], 766)
#         for l in f:
#             line = l.lower().strip().split(' ')
#             if not re.match(line, "#"):
#                 c = line[0]
#                 for i in index["dungeons"]:
#                     current = blizzard.game_mythic_keystone_leaderboard(i["id"], 766)
#                     for i in current["leading_groups"]:
#                         for j in i["members"]:
#                             if str(j["profile"]["name"]).lower() == str(c).lower():
#                                 print((j["profile"]["name"]).lower(), end = " ")
#                                 print(i["ranking"])


# mythic_plus()

def gen_random_image():
    """ Images for the side bar of the site """
    with open('character_list', 'r') as f:
        for i in f:
            line = i.lower().strip().split(' ')
            if line[0] != "#":
                main = True
                key = line[1]
                if len(line) == 3:
                    rl = True



def gen_team_table_html():
    with open('team_table.html', 'w') as f:
        f.write("<div class=\"w3-row-padding w3-center\">\n")
        for c in all_characters:
            f.write("<div class=\"w3-col m3\"><img src=\".img/" + c.player_name + "_bust.jpg\"" + " style=\"width:100%\" onclick=\"onClick(this)\" class=\"w3-hover-opacity\" alt=\"" + c.player_name + "\"></div>\n")
        f.write("</div>\n")


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
            "   <table style=\"background-color:#000000;color:black;\">\n"
            "   <th style=\"background-color:gray\">Name</th>\n"
            "   <th style=\"background-color:gray\">Head</th>\n"
            "   <th style=\"background-color:gray\">Neck</th>\n"
            "   <th style=\"background-color:gray\">Shoulder</th>\n"
            "   <th style=\"background-color:gray\">Chest</th>\n"
            "   <th style=\"background-color:gray\">Waist</th>\n"
            "   <th style=\"background-color:gray\">Legs</th>\n"
            "   <th style=\"background-color:gray\">Feet</th>\n"
            "   <th style=\"background-color:gray\">Wrist</th>\n"
            "   <th style=\"background-color:gray\">Hands</th>\n"
            "   <th style=\"background-color:gray\">Ring</th>\n"
            "   <th style=\"background-color:gray\">Ring</th>\n"
            "   <th style=\"background-color:gray\">Trinket</th>\n"
            "   <th style=\"background-color:gray\">Trinket</th>\n"
            "   <th style=\"background-color:gray\">Back</th>\n"
            "   <th style=\"background-color:gray\">Main Hand</th>\n"
            "   <th style=\"background-color:gray\">Off Hand</th>\n"
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
