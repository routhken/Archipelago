from . import GrimDawnTestBase, grimDawnOptionErrorTestBase
import unittest


class TestGoal0(GrimDawnTestBase):
    options = {
        "goal": 0,
    }


class TestGoal1(GrimDawnTestBase):
    options = {
        "goal": 1,
        "dlc_fg": True
    }

class TestGoal2(grimDawnOptionErrorTestBase,unittest.TestCase):
    options = {
        "goal": 1,
        "dlc_fg": False
    }

class TestGoal3(grimDawnOptionErrorTestBase,unittest.TestCase):
    options = {
        "goal": 4,
        "dlc_aom": False
    }

class TestGoal4(grimDawnOptionErrorTestBase,unittest.TestCase):
    options = {
        "goal": 50,
        "dlc_aom": False
    }


class TestGoal4DLC(GrimDawnTestBase):
    options = {
        "goal": 4,
        "dlc_aom": True,
        "dlc_fg": True
    }
class TestGoal4Dungeons(GrimDawnTestBase):
    options = {
        "goal": 4,
        "dlc_aom": True,
        "forbidden_dungeons": True
    }
class TestGoal4OneShot(GrimDawnTestBase):
    options = {
        "goal": 4,
        "dlc_aom": True,
        "one_shot": True
    }
class TestGoal4SecretChest(GrimDawnTestBase):
    options = {
        "goal": 4,
        "dlc_aom": True,
        "secret_chest": True
    }
class TestGoal4Shrine(GrimDawnTestBase):
    options = {
        "goal": 4,
        "dlc_aom": True,
        "devotion_shrine": True
    }
class TestGoal4Lore(GrimDawnTestBase):
    options = {
        "goal": 4,
        "dlc_aom": True,
        "lore": True
    }
class TestGoal4Faction(GrimDawnTestBase):
    options = {
        "goal": 4,
        "dlc_aom": True,
        "faction": True
    }
class TestGoal4Faction(GrimDawnTestBase):
    options = {
        "goal": 4,
        "dlc_aom": True,
        "dlc_fg": True,
        "forbidden_dungeons": True,
        "one_shot": True,
        "secret_chest": True,
        "devotion_shrine": True,
        "faction": True,
        "lore": True
    }

class TestFuzz1(GrimDawnTestBase):
    options = {
        "accessibility": "full",
        "goal": "emblem_hunt",
        "max_emblems": 32,
        "required_emblems": 73,
        "forbidden_dungeons": False,
        "one_shot": True,
        "secret_chest": True,
        "devotion_shrine": False,
        "lore": False,
        "block_flooded_passage": False,
        "progressive_progression": False,
        "faction": False,
        "dlc_aom": False,
        "dlc_fg": True,
        "dlc_foa": True
    }

class TestFuzz2(GrimDawnTestBase):
    options = {
        "accessibility": "full",
        "goal": "beat_beronath",
        "max_emblems": 95,
        "required_emblems": 61,
        "forbidden_dungeons": 'false',
        "one_shot": 'false',
        "secret_chest": 'true',
        "devotion_shrine": 'false',
        "lore": 'false',
        "block_flooded_passage": 'false',
        "progressive_progression": 'true',
        "faction": 'true',
        "dlc_aom": 'true',
        "dlc_fg": 'true',
        "dlc_foa": 'true'
    }

class TestFuzz3(GrimDawnTestBase):
    options = {
        "accessibility": "minimal",
        "goal": "beat_beronath",
        "max_emblems": 78,
        "required_emblems": 93,
        "forbidden_dungeons": 'false',
        "one_shot": 'false',
        "secret_chest": 'false',
        "devotion_shrine": 'true',
        "lore": 'false',
        "block_flooded_passage": 'true',
        "progressive_progression": 'false',
        "faction": 'true',
        "dlc_aom": 'false',
        "dlc_fg": 'true',
        "dlc_foa": 'true'
    }

class TestFuzz4(grimDawnOptionErrorTestBase,unittest.TestCase):
    options = {
        "accessibility": "full",
        "goal": "beat_all_bosses",
        "max_emblems": 2,
        "required_emblems": 98,
        "forbidden_dungeons": 'false',
        "one_shot": 'true',
        "secret_chest": 'true',
        "devotion_shrine": 'false',
        "lore": 'false',
        "block_flooded_passage": 'true',
        "progressive_progression": 'false',
        "faction": 'false',
        "dlc_aom": 'true',
        "dlc_fg": 'true',
        "dlc_foa": 'false',
    }

class TestFuzz5(GrimDawnTestBase):
    options = {
        "accessibility": "full",
        "goal": "beat_loghorrean",
        "max_emblems": 3,
        "required_emblems": 40,
        "forbidden_dungeons": 'true',
        "one_shot": 'false',
        "secret_chest": 'true',
        "devotion_shrine": 'false',
        "lore": 'false',
        "block_flooded_passage": 'false',
        "progressive_progression": 'false',
        "faction": 'false',
        "dlc_aom": 'false',
        "dlc_fg": 'false',
        "dlc_foa": 'true',
    }

class TestFuzz6(GrimDawnTestBase):
    options = {
        "accessibility": "minimal",
        "goal": "beat_master_of_flesh",
        "max_emblems": 3,
        "required_emblems": 72,
        "forbidden_dungeons": 'true',
        "one_shot": 'true',
        "secret_chest": 'false',
        "devotion_shrine": 'true',
        "lore": 'true',
        "block_flooded_passage": 'true',
        "progressive_progression": 'true',
        "faction": 'true',
        "dlc_aom": 'true',
        "dlc_fg": 'true',
        "dlc_foa": 'true',
    }

class TestFuzz7(GrimDawnTestBase):
    options = {
        "accessibility": "full",
        "goal": "beat_ravna",
        "max_emblems": 51,
        "required_emblems": 33,
        "forbidden_dungeons": 'true',
        "one_shot": 'true',
        "secret_chest": 'true',
        "devotion_shrine": 'false',
        "lore": 'false',
        "block_flooded_passage": 'true',
        "progressive_progression": 'false',
        "faction": 'true',
        "dlc_aom": 'false',
        "dlc_fg": 'true',
        "dlc_foa": 'true',
    }

class TestFuzz8(GrimDawnTestBase):
    options = {
        "accessibility": "minimal",
        "goal": "beat_ravna",
        "max_emblems": 19,
        "required_emblems": 32,
        "forbidden_dungeons": 'false',
        "one_shot": 'true',
        "secret_chest": 'false',
        "devotion_shrine": 'true',
        "lore": 'false',
        "block_flooded_passage": 'true',
        "progressive_progression": 'true',
        "faction": 'false',
        "dlc_aom": 'true',
        "dlc_fg": 'false',
        "dlc_foa": 'true',
    }

class TestFuzz9(GrimDawnTestBase):
    #seed = 40831675872273486146
    options = {
        "accessibility": "minimal",
        "goal": "emblem_hunt",
        "max_emblems": 91,
        "required_emblems": 69,
        "forbidden_dungeons": 'false',
        "one_shot": 'true',
        "secret_chest": 'false',
        "devotion_shrine": 'false',
        "lore": 'false',
        "block_flooded_passage": 'false',
        "progressive_progression": 'true',
        "faction": 'true',
        "dlc_aom": 'true',
        "dlc_fg": 'false',
        "dlc_foa": 'true',
    }

class TestFuzz10(GrimDawnTestBase):
    options = {
        "progression_balancing": 17,
        "accessibility": "full",
        "goal": "beat_warden",
        "max_emblems": 64,
        "required_emblems": 57,
        "forbidden_dungeons": 'false',
        "one_shot": 'true',
        "secret_chest": 'false',
        "devotion_shrine": 'false',
        "lore": 'false',
        "block_flooded_passage": 'true',
        "progressive_progression": 'true',
        "faction": 'false',
        "dlc_aom": 'true',
        "dlc_fg": 'false',
        "dlc_foa": 'false',
    }

class TestFuzz11(GrimDawnTestBase):
    options = {
        "progression_balancing": 33,
        "accessibility": "minimal",
        "goal": "beat_loghorrean",
        "max_emblems": 93,
        "required_emblems": 29,
        "forbidden_dungeons": 'false',
        "one_shot": 'true',
        "secret_chest": 'false',
        "devotion_shrine": 'true',
        "lore": 'true',
        "block_flooded_passage": 'true',
        "progressive_progression": 'true',
        "faction": 'true',
        "dlc_aom": 'false',
        "dlc_fg": 'false',
        "dlc_foa": 'true',
    }

class TestFuzz12(GrimDawnTestBase):
    seed = 84740401707282965932
    #seed = 951587118
    options = {
        "progression_balancing": 0,
        "accessibility": "full",
        "goal": "beat_loghorrean",
        "max_emblems": 39,
        "required_emblems": 6,
        "forbidden_dungeons": 'false',
        "one_shot": 'true',
        "secret_chest": 'true',
        "devotion_shrine": 'true',
        "lore": 'false',
        "block_flooded_passage": 'true',
        "progressive_progression": 'true',
        "faction": 'true',
        "dlc_aom": 'true',
        "dlc_fg": 'false',
        "dlc_foa": 'true',
        "skill_shuffler": 'false',
        "skill_balance_randomizer": 'false',
        "devotion_balance_randomizer": 'false',
        "skill_balance_range": "extreme",
        "skill_balance_weight": "mostly_buffs",
        "skill_balance_preserve_damage": 'true',
        "skill_balance_preserve_area": 'true',
        "skill_balance_preserve_duration": 'false',
        "skill_balance_preserve_mana": 'true',
        "skill_balance_preserve_projectiles": 'false',
        "skill_balance_preserve_cooldown": 'false',
        "skill_balance_preserve_chance": 'true',
        "skill_balance_preserve_defense": 'true',
        "skill_balance_preserve_summons": 'false',
        "skill_balance_preserve_speed": 'true',
        "pets_forever": 'false',
        "ultra_rapid_fire": 'true',
        "starting_skill_points": 'true',
        "free_skill_respec": 'true',
        "easy_shrine_cost": 'true',
        "enemy_randomizer": 'true',
        "dangerous_enemies": 'false',
        "third_person_camera": 'true',
        "custom_gear": 'true',
        "generic_gear_quality": "generous",
        "buff_enemies": "weakest",
        "trap_percent": 40,
        "trap_weights"
            "Slowness Trap": 76,
            "Literature Trap": 342,
        "death_link": 'true',
        "local_items": [],
        "non_local_items": [],
        "start_inventory": {},
        "start_hints": [],
        "start_location_hints": [],
        "exclude_locations": [],
        "priority_locations": [],
        "item_links": [],
        "plando_items": [],
    }

class TestFuzz13(GrimDawnTestBase):
    options = {
        "accessibility": "minimal",
        "goal": "emblem_hunt",
        "max_emblems": 100,
        "required_emblems": 100,
        "forbidden_dungeons": 'false',
        "one_shot": 'false',
        "secret_chest": 'false',
        "devotion_shrine": 'false',
        "lore": 'false',
        "block_flooded_passage": 'true',
        "progressive_progression": 'false',
        "faction": 'false',
        "dlc_aom": 'false',
        "dlc_fg": 'false',
        "dlc_foa": 'false',
        "trap_percent": 50,
        "plando_items"
            # "item": "Wightmire Bridge Repair",
            #     "location": "Warden Krieg",
            #     "percentage": 100,
            #     "world": "false",
            #     "force": "true",
            "item": "Arkovia Bridge Repair",
                "location": "Darius Cronely",
                "percentage": 100,
                "world": "false",
                "force": "true",
    }
