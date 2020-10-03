from blizzard import Blizzard
import json
import time
import os
import re

blizzard = Blizzard()

specialization = {
    62: ["mage", "arcane", "damage", "range"],
    63: ["mage", "fire", "damage", "range"],
    64: ["mage", "frost", "damage", "range"],
    65: ["paladin", "holy", "healer", "range"],
    66: ["paladin", "protection", "tank", "melee"],
    70: ["paladin", "retribution", "damage", "melee"],
    71: ["warrior", "arms", "damage", "melee"],
    72: ["warrior", "fury", "damage", "melee"],
    73: ["warrior", "protection", "tank", "melee"],
    102: ["druid", "balance", "damage", "range"],
    103: ["druid", "feral", "damage", "melee"],
    104: ["druid", "guardian", "tank", "melee"],
    105: ["druid", "restoration", "damage", "range"],
    250: ["death knight", "blood", "tank", "melee"],
    251: ["death knight", "frost", "damage", "melee"],
    252: ["death knight", "unholy" "tank", "melee"],
    253: ["hunter", "beast mastery", "damage", "range"],
    254: ["hunter", "marksmanship", "damage", "range"],
    255: ["hunter", "survival", "damage", "melee"],
    256: ["priest", "discipline", "healer", "range"],
    257: ["priest", "holy", "healer", "range"],
    258: ["priest", "shadow", "damage", "range"],
    259: ["rogue", "assassination", "damage", "melee"],
    260: ["rogue", "outlaw", "damage", "melee"],
    261: ["rogue", "subtlety", "damage", "melee"],
    262: ["shaman", "elemental", "damage", "range"],
    263: ["shaman", "enhancement", "damage", "range"],
    264: ["shaman", "restoration", "healer", "range"],
    265: ["warlock", "affliction", "damage", "range"],
    266: ["warlock", "demonology", "damage", "range"],
    267: ["warlock", "destruction", "damage", "range"],
    268: ["monk", "brewmaster", "tank", "melee"],
    269: ["monk", "windwalker", "damage", "melee"],
    270: ["monk", "mistweaver", "healer", "range"],
    577: ["demon hunter", "havoc" "tank", "melee"],
    581: ["demon hunter", "vengeance", "damage", "melee"]
}


def history(current_period=True):
    period_index_call = blizzard.game_mythic_keystone_period_index()
    dungeon_index_call = blizzard.game_mythic_keystone_dungeons_index()

    period_index = []
    dungeon_index = {}

    for p_index in period_index_call["periods"]:
        period_index.append(p_index["id"])

    for d_index in dungeon_index_call["dungeons"]:
        dungeon_index[d_index["id"]] = d_index["name"]

    if current_period:
        period_index = period_index[-1]
    else:
        pass

    for p in period_index:
        for d in dungeon_index:
            try:
                leaderboard = blizzard.game_mythic_keystone_leaderboard(d, p)
                for leader in leaderboard["leading_groups"]:
                    with open('character_list', 'r') as f:
                        key = ""
                        for player in f:
                            line = player.lower().split(' ')
                            if line[0] == "#":
                                key = line[1].strip()
                            else:
                                current_run = []
                                for member in leader["members"]:
                                    if member["profile"]["name"].lower() == player.split(' ')[0].lower():
                                        current_run.append(key)
                                        current_run.append(",")
                                        current_run.append(leader["keystone_level"])
                                        current_run.append(",")
                                        current_run.append(leaderboard["map"]["name"])
                                        current_run.append(",")
                                        current_run.append(leaderboard["period"])
                                        current_run.append(",")
                                        current_run.append(leader["duration"])
                                        current_run.append(",")
                                        current_run.append(leader["completed_timestamp"])
                                        current_run.append(",")

                                        for m in leader["members"]:
                                            current_run.append(m["profile"]["name"])
                                            current_run.append(",")
                                            for s in specialization[m["specialization"]["id"]]:
                                                current_run.append(s)
                                                current_run.append(",")
                                        for affix in leaderboard["keystone_affixes"]:
                                            current_run.append(affix["keystone_affix"]["name"])
                                            current_run.append(",")
                                        with open('m_pluse_data.txt', 'a') as mpd:
                                            for line in current_run:
                                                mpd.write(str(line))
                                            mpd.write('\n')
            except Exception as e:
                print("\nCould not parse " + str(dungeon_index[d] + " " + str(d) + " " + str(p)))
                break


history(False)
