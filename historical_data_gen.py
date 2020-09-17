from blizzard import Blizzard
import json
import time
import os

blizzard = Blizzard()

period_index_call = blizzard.game_mythic_keystone_period_index()
dungeon_index_call = blizzard.game_mythic_keystone_dungeons_index()

period_index=[]
dungeon_index = {}

for p_index in period_index_call["periods"]:
    period_index.append(p_index["id"])

for d_index in dungeon_index_call["dungeons"]:
    dungeon_index[d_index["id"]] = d_index["name"]

# There seems to be nothing for the starting period index untill 651
# for p in period_index:
#     print("### working on period " + str(p) + " ###")
#     for d in dungeon_index:
#         print("working on " + str(dungeon_index[d]), end=': ')
#         record = blizzard.game_mythic_keystone_leaderboard(d, p)
#         if record is not None:
#             with open('historical_data/bfa/season_4/' + str(p) + "_" + str(dungeon_index[d]), 'w') as f:
#                 f.write(str(record).replace(" ", "").strip())
#                 print("Writing")
#         else: print("There is nothing here")
#         time.sleep(1.05)


# The above loop kind of messed up the data and I'm not got to make changes and re-test.
# The following will get the data back in working order

# import os
# import re
# location = "historical_data/bfa/season_4/"

# for i in os.walk(location):
#     current = ''
#     for j in i:
#         for k in j:
#             if len(k) > 2:
#                 print(k)
#                 f = open(location + k, 'r')
#                 data = f.read()
#                 f.close()

#                 new_data = data.replace('\'', '\"')
#                 f = open(location + k, 'w')
#                 f.write(new_data)
#                 f.close()




# f = open('historical_data/bfa/season_4/766_Freehold', 'r')
# test = f.read()
# test = json.loads(test)
# print(test["profile"])

print(period_index)

