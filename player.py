import os
import urllib.parse
import urllib.request
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class Player:

    def __init__(self, main, rl, player_info, gear_info, profession_info, pvp_2s, pvp_3s, image_url, player_id):

        ### PLAYER GENERAL INFO ###
        self.player_main = main
        self.player_rl = rl
        self.player_name = urllib.parse.unquote(player_info["name"])
        self.player_class = player_info["character_class"]["name"]
        self.player_spec = player_info["active_spec"]["name"]
        self.player_level = player_info["level"]
        self.player_equipped_item_level = player_info["equipped_item_level"]
        self.player_average_item_level = player_info["average_item_level"]
        try:
            self.player_title = str(player_info["active_title"]["display_string"]).replace("{name}", self.player_name)
        except:
            self.player_title = None

        c = str.upper(self.player_class)
        if c == "WARRIOR":
            self.class_color = "#C79C6E"
        elif c == "MAGE":
            self.class_color ="#40C7EB"
        elif c == "ROGUE":
            self.class_color ="#FFF569"
        elif c == "DRUID":
            self.class_color ="#FF7D0A"
        elif c == "WARLOCK":
            self.class_color ="#8787ED"
        elif c == "SHAMAN":
            self.class_color ="#0070DE"
        elif c == "MONK":
            self.class_color ="#00FF96"
        elif c == "HUNTER":
            self.class_color ="#A9D271"
        elif c == "PALADIN":
            self.class_color ="#F58CBA"
        elif c == "DEMON HUNTER":
            self.class_color ="#A330C9"
        elif c == "DEATH KNIGHT":
            self.class_color ="#C41F3B"
        elif c == "PRIEST":
            self.class_color ="#FFFFFF"

        ### PLAYER GEAR ###
        self.gear_list = []

        for item in gear_info["equipped_items"]:
            temp = []
            temp.append(item["slot"]["type"])
            temp.append(item["slot"]["name"])
            c = str.upper(item["quality"]["type"])
            if c == "UNCOMMON":
                temp.append("#1eff00")
            elif c == "RARE":
                temp.append("#0070dd")
            elif c == "EPIC":
                temp.append("#a335ee")
            elif c== "LEGENDARY":
                temp.append("#ff8000")
            elif c == "ARTIFACT":
                temp.append("#e6cc80")
            temp.append(item["quality"]["type"])
            temp.append(item["level"]["value"])
            self.gear_list.append(temp)

        ### PLAYER PROFESSION ###
        self.profession_list = []
        
        if "primaries" in profession_info:
            for item in profession_info["primaries"]:
                temp = []
                temp.append(item["profession"]["name"])
                temp.append(item["tiers"][0]["skill_points"])
                temp.append(item["tiers"][0]["max_skill_points"])
                temp.append(item["tiers"][0]["tier"]["name"])
                self.profession_list.append(temp)

        ### PLAYER PVP ###
        MIN_SCORE_TO_DISPLAY = 1200

        if isinstance(pvp_2s, int) and  isinstance(pvp_3s, int):
            self.pvp_2s = pvp_2s
            self.pvp_3s = pvp_3s
            if pvp_2s > pvp_3s and pvp_2s >= MIN_SCORE_TO_DISPLAY:
                self.pvp_highest = pvp_2s
            elif pvp_3s > pvp_2s and pvp_3s >= MIN_SCORE_TO_DISPLAY:
                self.pvp_highest = pvp_3s
            else: self.pvp_highest = 0

        ### IMAGE URL ###
        self.avatar = image_url["avatar_url"]
        self.bust = image_url["bust_url"]
        self.render = image_url["render_url"]

        ### Player ID ###
        self.player_id = player_id

    def get_bust(self):
        urllib.request.urlretrieve(self.bust, '.img/' + self.player_name + '_bust.jpg')

    def get_avatiar(self):
        urllib.request.urlretrieve(self.avatar, '.img/' + self.player_name + '_avatiar.jpg')

    def get_render(self):
        urllib.request.urlretrieve(self.render, '.img/' + self.player_name + '_render.jpg')

    def create_image(self):
        print("Generating image for: " + str(self.player_name))
        IMG_BOARDER = 10
        
        self.get_bust()

        with Image.open('.img/' + self.player_name + '_bust.jpg') as img1:
            w, h = img1.size
            background = Image.new('RGB', (w + 2 * IMG_BOARDER, h + 2 * IMG_BOARDER), self.class_color)
            background.save('.img/background.jpg')

            img1 = Image.open('.img/background.jpg')
            img2 = Image.open('.img/' + self.player_name + '_bust.jpg')
            img1.paste(img2, (IMG_BOARDER, IMG_BOARDER))
            img1.save(".img/" + self.player_name + "_bust.jpg")

        with Image.open('.img/' + self.player_name + '_bust.jpg') as img1:
            w, h = img1.size
            draw = ImageDraw.Draw(img1)
            font = ImageFont.truetype(".fount/arial.ttf", 26)
            W, H = draw.textsize(self.player_name, font=font)

            draw.text(((w - W) / 2 - 1, (h - H) - 1), self.player_name, font=font, fill="black")
            draw.text(((w - W) / 2 - 1, (h - H) + 1), self.player_name, font=font, fill="black")
            draw.text(((w - W) / 2 + 1, (h - H) + 1), self.player_name, font=font, fill="black")
            draw.text(((w - W) / 2 + 1, (h - H) - 1), self.player_name, font=font, fill="black")
            draw.text(((w - W) / 2, (h - H)), self.player_name, font=font, fill=self.class_color)
            img1.save(".img/" + self.player_name + "_bust.jpg")
