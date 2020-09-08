import requests
import json
import time
import os


insert_time = False

def sleep():
  if insert_time:
    time.sleep(1)

class Blizzard:

  api_count = 0

  def __init__(self):
    CLIENT = os.environ['CLIENT']
    SECRET = os.environ['SECRET']
    self.access_token = requests.get("https://us.battle.net/oauth/token?grant_type=client_credentials&client_id=" + CLIENT + "&client_secret=" + SECRET).json()["access_token"]

  ### Game API Call ###
  def game_mythic_keystone_season_index (self): # name good
    # return a single int of the current m plus season
    self.api_count += 1
    sleep()
    self.current_season = requests.get("https://us.api.blizzard.com/data/wow/mythic-keystone/season/index?namespace=dynamic-us&locale=en_US&access_token=" + self.access_token)
    if self.current_season.status_code == 200:
      return json.loads(self.current_season.text)["current_season"]["id"]
    else: return None

  def game_profession_index(self):
    # return json blob of profession id and name
    self.api_count += 1
    sleep()
    self.p_name = requests.get("https://us.api.blizzard.com/data/wow/profession/index?namespace=static-us&locale=en_US&access_token=" + self.access_token)
    if self.p_name.status_code == 200:
        return json.loads(self.p_name.text)
    else: return None

  def game_profession(self, n):
    # return a string of the current tier profession names, where n is the profession id
    self.api_count += 1
    sleep()
    self.p_tier = requests.get("https://us.api.blizzard.com/data/wow/profession/" + str(n) + "?namespace=static-us&locale=en_US&access_token=" + self.access_token)
    if self.p_tier.status_code == 200:
      return json.loads(self.p_tier.text)["skill_tiers"][0]["name"]
    else: return None

  def game_mythic_keystone_dungeons_index(self):
    self.api_count += 1
    sleep()
    self.dungeon = requests.get("https://us.api.blizzard.com/data/wow/mythic-keystone/dungeon/index?namespace=dynamic-us&locale=en_US&access_token=" + self.access_token)
    if self.dungeon.status_code == 200:
      return json.loads(self.dungeon.text)
    else: return None

  def game_mythic_keystone_period_index(self):
    self.api_count += 1
    sleep()
    self.dungeon = requests.get("https://us.api.blizzard.com/data/wow/mythic-keystone/dungeon/index?namespace=dynamic-us&locale=en_US&access_token=" + self.access_token)
    if self.dungeon.status_code == 200:
      return json.loads(self.dungeon.text)
    else: return None

  def game_mythic_keystone_leaderboard(self, n=1427): #1427 is the connected relm id for a-p
    self.api_count += 1
    sleep()
    self.dungeon = requests.get("https://us.api.blizzard.com/data/wow/connected-realm/" + str(n) + "/mythic-leaderboard/index?namespace=dynamic-us&locale=en_US&access_token=" + self.access_token)
    if self.dungeon.status_code == 200:
      return json.loads(self.dungeon.text)
    else: return None

  ### Profile API Call ###
  def profile_character_equipment(self, player, server):
    # return a json blob of a player's currently equiped gear.
    self.api_count += 1
    sleep()
    self.p_gear = requests.get("https://us.api.blizzard.com/profile/wow/character/" + server + "/" + player + "/equipment?namespace=profile-us&locale=en_US&access_token=" + self.access_token)
    if self.p_gear.status_code == 200:
      return json.loads(self.p_gear.text)
    else: return None

  def profile_character_profession(self, name, server):
    self.api_count += 1
    sleep()
    self.p_player = requests.get("https://us.api.blizzard.com/profile/wow/character/" + server + "/" + name + "/professions?namespace=profile-us&locale=en_US&access_token=" + self.access_token)
    if self.p_player.status_code == 200:
      return json.loads(self.p_player.text)
    else: return None

  def profile_character_profile(self, name, server):
    self.api_count += 1
    sleep()
    self.profile = requests.get("https://us.api.blizzard.com/profile/wow/character/" + server + "/" + name + "?namespace=profile-us&locale=en_US&access_token=" + self.access_token)
    if self.profile.status_code == 200:
        return json.loads(self.profile.text)
    else: return None

  def profile_character_pvp(self, name, server, bracket):
    self.api_count += 1
    sleep()
    self.pvp = requests.get("https://us.api.blizzard.com/profile/wow/character/" + server + "/" + name + "/pvp-bracket/" + bracket +"?namespace=profile-us&locale=en_US&access_token=" + self.access_token)
    if self.pvp.status_code == 200:
      return json.loads(self.pvp.text)["rating"]
    else: return 0

  ### Other ### 
  def image_render(self, name, server):
    self.api_count += 1
    sleep()
    self.render = requests.get("https://us.api.blizzard.com/profile/wow/character/" + server + "/" + name + "/character-media?namespace=profile-us&locale=en_US&access_token=" + self.access_token)
    if self.render.status_code == 200:
      return json.loads(self.render.text)
    else: return None