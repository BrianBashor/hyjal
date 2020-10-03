import requests
import json
import os


class Blizzard:

    api_count = 0

    def __init__(self):
        """Create access token."""
        CLIENT = os.environ['CLIENT']
        SECRET = os.environ['SECRET']
        self.access_token = requests.get("https://us.battle.net/oauth/token?grant_type=client_credentials&client_id=" + CLIENT + "&client_secret=" + SECRET).json()["access_token"]

    # Game API Call #
    def game_mythic_keystone_season_index(self):
        self.api_count += 1
        self.current_season = requests.get("https://us.api.blizzard.com/data/wow/mythic-keystone/season/index?namespace=dynamic-us&locale=en_US&access_token=" + self.access_token)
        if self.current_season.status_code == 200:
            return json.loads(self.current_season.text)
        else:
            return None

    def game_profession_index(self):
        self.api_count += 1
        self.p_name = requests.get("https://us.api.blizzard.com/data/wow/profession/index?namespace=static-us&locale=en_US&access_token=" + self.access_token)
        if self.p_name.status_code == 200:
            return json.loads(self.p_name.text)
        else:
            return None

    def game_profession(self, n):
        self.api_count += 1
        self.p_tier = requests.get("https://us.api.blizzard.com/data/wow/profession/" + str(n) + "?namespace=static-us&locale=en_US&access_token=" + self.access_token)
        if self.p_tier.status_code == 200:
            return json.loads(self.p_tier.text)
        else:
            return None

    def game_mythic_keystone_dungeons_index(self):
        self.api_count += 1
        self.dungeon = requests.get("https://us.api.blizzard.com/data/wow/mythic-keystone/dungeon/index?namespace=dynamic-us&locale=en_US&access_token=" + self.access_token)
        if self.dungeon.status_code == 200:
            return json.loads(self.dungeon.text)
        else:
            return None

    def game_mythic_keystone_period_index(self):
        self.api_count += 1
        self.dungeon = requests.get("https://us.api.blizzard.com/data/wow/mythic-keystone/period/index?namespace=dynamic-us&locale=en_US&access_token=" + self.access_token)
        if self.dungeon.status_code == 200:
            return json.loads(self.dungeon.text)
        else:
            return None

    def game_mythic_keystone_leaderboard(self, dungeon_id, period, cr_id=1426):
        self.api_count += 1
        self.dungeon = requests.get("https://us.api.blizzard.com/data/wow/connected-realm/" + str(cr_id) + "/mythic-leaderboard/" + str(dungeon_id) + "/period/" + str(period) + "?namespace=dynamic-us&locale=en_US&access_token=" + self.access_token)
        if self.dungeon.status_code == 200:
            return json.loads(self.dungeon.text)
        else:
            return None

    def game_playable_specialization(self, id):
        self.api_count += 1
        self.spec = requests.get("https://us.api.blizzard.com/data/wow/playable-specialization/" + str(id) + "?namespace=static-us&locale=en_US&access_token=" + self.access_token)
        if self.spec.status_code == 200:
            return json.loads(self.spec.text)
        else:
            return None

    def game_playable_specialization_index(self):
        self.api_count += 1
        self.spec = requests.get("https://us.api.blizzard.com/data/wow/playable-specialization/index?namespace=static-us&locale=en_US&access_token=" + self.access_token)
        if self.spec.status_code == 200:
            return json.loads(self.spec.text)
        else:
            return None

    def external_call(self, url):
        self.api_count += 1
        self.external = requests.get(url + "&access_token=" + self.access_token)
        if self.external.status_code == 200:
            return json.loads(self.external.text)
        else:
            print("something went wrong")
            return None

    # Profile API Call #
    def profile_character_equipment(self, player, server):
        self.api_count += 1
        self.p_gear = requests.get("https://us.api.blizzard.com/profile/wow/character/" + server + "/" + player + "/equipment?namespace=profile-us&locale=en_US&access_token=" + self.access_token)
        if self.p_gear.status_code == 200:
            return json.loads(self.p_gear.text)
        else:
            return None

    def profile_character_profession(self, name, server):
        self.api_count += 1
        self.p_player = requests.get("https://us.api.blizzard.com/profile/wow/character/" + server + "/" + name + "/professions?namespace=profile-us&locale=en_US&access_token=" + self.access_token)
        if self.p_player.status_code == 200:
            return json.loads(self.p_player.text)
        else:
            return None

    def profile_character_profile(self, name, server):
        self.api_count += 1
        self.profile = requests.get("https://us.api.blizzard.com/profile/wow/character/" + server + "/" + name + "?namespace=profile-us&locale=en_US&access_token=" + self.access_token)
        if self.profile.status_code == 200:
            return json.loads(self.profile.text)
        else:
            return None

    def profile_character_pvp(self, name, server, bracket):
        self.api_count += 1
        self.pvp = requests.get("https://us.api.blizzard.com/profile/wow/character/" + server + "/" + name + "/pvp-bracket/" + bracket + "?namespace=profile-us&locale=en_US&access_token=" + self.access_token)
        if self.pvp.status_code == 200:
            return json.loads(self.pvp.text)["rating"]
        else:
            return 0

    def profile_character_media(self, name, server):
        self.api_count += 1
        self.render = requests.get("https://us.api.blizzard.com/profile/wow/character/" + server + "/" + name + "/character-media?namespace=profile-us&locale=en_US&access_token=" + self.access_token)
        if self.render.status_code == 200:
            return json.loads(self.render.text)
        else:
            return None

    def profile_specialization(self, url):
        self.api_count += 1
        self.spec = requests.get(url)
        if self.spec.status_code == 200:
            return json.loads(self.spec.text + "&access_token=" + self.access_token)
        else:
            return None
