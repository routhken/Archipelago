from . import GrimDawnTestBase


class TestGoal0(GrimDawnTestBase):
    options = {
        "goal": 0,
    }


class TestGoal1(GrimDawnTestBase):
    options = {
        "goal": 1,
        "dlc_fg": True
    }


class TestGoal4DLC(GrimDawnTestBase):
    options = {
        "goal": 4,
        "dlc_fg": True
    }
class TestGoal4Dungeons(GrimDawnTestBase):
    options = {
        "goal": 4,
        "forbidden_dungeons": True
    }
class TestGoal4OneShot(GrimDawnTestBase):
    options = {
        "goal": 4,
        "one_shot": True
    }
class TestGoal4SecretChest(GrimDawnTestBase):
    options = {
        "goal": 4,
        "secret_chest": True
    }
class TestGoal4Shrine(GrimDawnTestBase):
    options = {
        "goal": 4,
        "devotion_shrine": True
    }
class TestGoal4Lore(GrimDawnTestBase):
    options = {
        "goal": 4,
        "lore": True
    }
class TestGoal4Faction(GrimDawnTestBase):
    options = {
        "goal": 4,
        "faction": True
    }
class TestGoal4Faction(GrimDawnTestBase):
    options = {
        "goal": 4,
        "dlc_fg": True,
        "forbidden_dungeons": True,
        "one_shot": True,
        "secret_chest": True,
        "devotion_shrine": True,
        "faction": True,
        "lore": True
    }
