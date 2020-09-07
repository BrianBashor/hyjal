import requests
import json
import time
import os

class Blizzard:

  api_count = 0
  insert_time = False

  def __init__(self):
    CLIENT = os.environ['CLIENT']
    SECRET = os.environ['SECRET']
    self.access_token = requests.get("https://us.battle.net/oauth/token?grant_type=client_credentials&client_id=" + CLIENT + "&client_secret=" + SECRET).json()["access_token"]

  def m_plus_current_season_num (self):
    self.api_count += 1
    if self.insert_time:
      time.sleep(1)
    self.current_season = requests.get("https://us.api.blizzard.com/data/wow/mythic-keystone/season/index?namespace=dynamic-us&locale=en_US&access_token=" + self.access_token)
    if self.current_season.status_code == 200:
      return json.loads(self.current_season.text)["current_season"]["id"]
    else: return None

  def player_gear(self, player, server):
    self.api_count += 1
    if self.insert_time:
      time.sleep(1)
    self.p_gear = requests.get("https://us.api.blizzard.com/profile/wow/character/" + server + "/" + player + "/equipment?namespace=profile-us&locale=en_US&access_token=" + self.access_token)
    if self.p_gear.status_code == 200:
      return json.loads(self.p_gear.text)
    else: return None

  def profession_name(self):
    self.api_count += 1
    if self.insert_time:
      time.sleep(1)
    self.p_name = requests.get("https://us.api.blizzard.com/data/wow/profession/index?namespace=static-us&locale=en_US&access_token=" + self.access_token)
    if self.p_name.status_code == 200:
        return json.loads(self.p_name.text)
    else: return None

  def profession_current_tier(self, n):
    self.api_count += 1
    if self.insert_time:
      time.sleep(1)
    n = str(n)
    self.p_tier = requests.get("https://us.api.blizzard.com/data/wow/profession/" + n + "?namespace=static-us&locale=en_US&access_token=" + self.access_token)
    if self.p_tier.status_code == 200:
      return json.loads(self.p_tier.text)["skill_tiers"][0]["name"]
    else: return None

  def profession_player(self, name, server):
    self.api_count += 1
    if self.insert_time:
      time.sleep(1)
    self.p_player = requests.get("https://us.api.blizzard.com/profile/wow/character/" + server + "/" + name + "/professions?namespace=profile-us&locale=en_US&access_token=" + self.access_token)
    if self.p_player.status_code == 200:
      return json.loads(self.p_player.text)
    else: return None

  def image_render(self, name, server):
    self.api_count += 1
    if self.insert_time:
      time.sleep(1)
    self.render = requests.get("https://us.api.blizzard.com/profile/wow/character/" + server + "/" + name + "/character-media?namespace=profile-us&locale=en_US&access_token=" + self.access_token)
    if self.render.status_code == 200:
      return json.loads(self.render.text)
    else: return None

  def player_profile(self, name, server):
    self.api_count += 1
    if self.insert_time:
      time.sleep(1)
    self.profile = requests.get("https://us.api.blizzard.com/profile/wow/character/" + server + "/" + name + "?namespace=profile-us&locale=en_US&access_token=" + self.access_token)
    if self.profile.status_code == 200:
        return json.loads(self.profile.text)
    else: return None

  def player_pvp(self, name, server, bracket):
    self.api_count += 1
    if self.insert_time:
      time.sleep(1)
    self.pvp = requests.get("https://us.api.blizzard.com/profile/wow/character/" + server + "/" + name + "/pvp-bracket/" + bracket +"?namespace=profile-us&locale=en_US&access_token=" + self.access_token)
    if self.pvp.status_code == 200:
      return json.loads(self.pvp.text)["rating"]
    else: return 0

  def m_plus_dungeon_index(self):
    self.api_count += 1
    if self.insert_time:
      time.sleep(1)
    self.dungeon = requests.get("https://us.api.blizzard.com/data/wow/mythic-keystone/dungeon/index?namespace=dynamic-us&locale=en_US&access_token=" + self.access_token)
    if self.dungeon.status_code == 200:
      return json.loads(self.dungeon.text)
    else: return None
