class Game_Data:

  def __init__(self, profession_info, m_plus_season_info, dungeon_info):
    self.current_m_plus_season = m_plus_season_info
  
    self.current_profession_id = []
    self.current_profession_name = []
    for p in profession_info["professions"]:
      self.current_profession_id.append(p["id"])
      self.current_profession_name.append(p["name"])

    self.dungeon_list = []
    for d in dungeon_info["dungeons"]:
      self.dungeon_list.append(d["name"])