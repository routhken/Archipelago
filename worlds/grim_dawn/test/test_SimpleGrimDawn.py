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
