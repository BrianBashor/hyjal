import urllib.parse
import urllib.request
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from blizzard import Blizzard
import json

blizzard = Blizzard()

class Player:
    def __init__(self, main, raid_lead, key, name, server):

        self.key = key
        self.main = main
        self.raid_lead = raid_lead

        ### PLAYER INFO ###
        player_info = blizzard.profile_character_profile(name, server)
        self.player_name = player_info["name"]
        self.player_race =  player_info["race"]["name"]
        self.player_class =  player_info["character_class"]["name"]
        self.player_spec = player_info["active_spec"]["name"]
        self.player_level = player_info["level"]

        if "active_title" in player_info.keys():
            self.player_title = player_info["active_title"]["display_string"].replace("{name}", self.player_name)
        else:
            self.player_title = None

        specialization = {
        62: ["damage", "range"],
        63: ["damage", "range"],
        64: ["damage", "range"],
        65: ["healer", "range"],
        66: ["tank", "melee"],
        70: ["damage", "melee"],
        71: ["damage", "melee"],
        72: ["damage", "melee"],
        73: ["tank", "melee"],
        102: ["damage", "range"],
        103: ["damage", "melee"],
        104: ["tank", "melee"],
        105: ["damage", "range"],
        250: ["tank", "melee"],
        251: ["damage", "melee"],
        252: ["damage", "melee"],
        253: ["damage", "range"],
        254: ["damage", "range"],
        255: ["damage", "melee"],
        256: ["healer", "range"],
        257: ["healer", "range"],
        258: ["damage", "range"],
        259: ["damage", "melee"],
        260: ["damage", "melee"],
        261: ["damage", "melee"],
        262: ["damage", "range"],
        263: ["damage", "range"],
        264: ["healer", "range"],
        265: ["damage", "range"],
        266: ["damage", "range"],
        267: ["damage", "range"],
        268: ["tank", "melee"],
        269: ["damage", "melee"],
        270: ["healer", "range"],
        577: ["tank", "melee"],
        581: ["damage", "melee"]
        }
        
        self.role = specialization[player_info["active_spec"]["id"]][0]
        self.role_type = specialization[player_info["active_spec"]["id"]][1]

        c = str.upper(self.player_class)
        if c == "WARRIOR":
            self.class_color = "#C79C6E"
        elif c == "MAGE":
            self.class_color = "#40C7EB"
        elif c == "ROGUE":
            self.class_color = "#FFF569"
        elif c == "DRUID":
            self.class_color = "#FF7D0A"
        elif c == "WARLOCK":
            self.class_color = "#8787ED"
        elif c == "SHAMAN":
            self.class_color = "#0070DE"
        elif c == "MONK":
            self.class_color = "#00FF96"
        elif c == "HUNTER":
            self.class_color = "#A9D271"
        elif c == "PALADIN":
            self.class_color = "#F58CBA"
        elif c == "DEMON HUNTER":
            self.class_color = "#A330C9"
        elif c == "DEATH KNIGHT":
            self.class_color = "#C41F3B"
        elif c == "PRIEST":
            self.class_color = "#FFFFFF"

        ### PLAYER GEAR ###
        gear_info = blizzard.profile_character_equipment(name, server)
        self.player_gear = []
        for item in gear_info["equipped_items"]:
            tmp = []
            tmp.append(item["slot"]["name"])
            c = str.upper(item["quality"]["type"])
            if c == "UNCOMMON":
                tmp.append("#1eff00")
            elif c == "RARE":
                tmp.append("#0070dd")
            elif c == "EPIC":
                tmp.append("#a335ee")
            elif c == "LEGENDARY":
                tmp.append("#ff8000")
            elif c == "ARTIFACT":
                tmp.append("#e6cc80")
            tmp.append(item["quality"]["type"])
            tmp.append(item["level"]["value"])
            self.player_gear.append(tmp)

        ### PLAYER PROFESSION ###
        profession_info = blizzard.profile_character_profession(name, server)
        self.profession_list = []
        if "primaries" in profession_info:
            for item in profession_info["primaries"]:
                tmp = []
                tmp.append(item["profession"]["name"])
                tmp.append(item["tiers"][0]["skill_points"])
                tmp.append(item["tiers"][0]["max_skill_points"])
                tmp.append(item["tiers"][0]["tier"]["name"])
                self.profession_list.append(tmp)

        # PLAYER PVP #
        MIN_SCORE_TO_DISPLAY = 1200
        pvp_2s = blizzard.profile_character_pvp(name, server, "2v2")
        pvp_3s = blizzard.profile_character_pvp(name, server, "3v3")

        if isinstance(pvp_2s, int) and isinstance(pvp_3s, int):
            self.pvp_2s = pvp_2s
            self.pvp_3s = pvp_3s
            if pvp_2s > pvp_3s and pvp_2s >= MIN_SCORE_TO_DISPLAY:
                self.pvp_highest = pvp_2s
            elif pvp_3s > pvp_2s and pvp_3s >= MIN_SCORE_TO_DISPLAY:
                self.pvp_highest = pvp_3s
            else:
                self.pvp_highest = 0

        ### IMAGE URL ###
        image_url = blizzard.profile_character_media(name, server)
        try:
            inset = image_url["assets"][1]["value"]
        except Exception as e:
            print(e)
            print("Player is inactive")

        ### TEAM PICTURE ###
        IMG_BOARDER = 10

        urllib.request.urlretrieve(inset, 'img/' + self.player_name + '_inset.jpg')

        with Image.open('img/' + self.player_name + '_inset.jpg') as img1:
            w, h = img1.size
            background = Image.new('RGB', (w + 2 * IMG_BOARDER, h + 2 * IMG_BOARDER), self.class_color)
            background.save('img/background.jpg', quality=100)

            img1 = Image.open('img/background.jpg')
            img2 = Image.open('img/' + self.player_name + '_inset.jpg')
            img1.paste(img2, (IMG_BOARDER, IMG_BOARDER))
            img1.save("img/" + self.player_name + "_inset.jpg", quality=100)

        with Image.open('img/' + self.player_name + '_inset.jpg') as img1:
            w, h = img1.size
            draw = ImageDraw.Draw(img1)
            font = ImageFont.truetype("fonts/LoveWhisper-Personal Use.ttf", 42)
            W, H = draw.textsize(self.player_name, font=font)

            draw.text(((w - W) / 2 - 1, (h - H) - 1), self.player_name, font=font, fill="black")
            draw.text(((w - W) / 2 - 1, (h - H) + 1), self.player_name, font=font, fill="black")
            draw.text(((w - W) / 2 + 1, (h - H) + 1), self.player_name, font=font, fill="black")
            draw.text(((w - W) / 2 + 1, (h - H) - 1), self.player_name, font=font, fill="black")
            draw.text(((w - W) / 2, (h - H + 1)), self.player_name, font=font, fill=self.class_color)
            img1.save("img/" + self.player_name + "_inset.jpg", quality=100)

