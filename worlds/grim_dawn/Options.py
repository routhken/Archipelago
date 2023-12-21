from typing import Dict

from Options import Choice, Option, Toggle, PerGameCommonOptions
from dataclasses import dataclass

class GrimDawnGoal(Choice):
    """
    The goal to accomplish in order to complete the seed.
    Beat Warden - Finish Act 1 and kill the Warden Krieg
    Beat Ravna - Finish Act 3 and kill Swarm Queen Ravna
    Beat Karroz - Finish Act 4 and kill Karroz, Sigil of Ch'thon
    """
    display_name = "Goal"

    option_beat_warden = 0
    option_beat_ravna = 1
    option_beat_karroz = 2

    default = 0

class GrimDawnForbiddenDungeons(Toggle):
    """Enable Forbidden Dungeons and Skeleton Keys as locations"""
    display_name="Forbidden Dungeons and Skeleton Keys"

class GrimDawnOneShot(Toggle):
    """Enable One Shot Chests as locations"""
    display_name="One Shot Chests"

class GrimDawnSecretChest(Toggle):
    """Enable Secret Chests as locations"""
    display_name="Secret Chests"

class GrimDawnDevotionShrines(Toggle):
    """Enable Devotion Shrines as locations"""
    display_name="Devotion Shrines"

class GrimDawnLore(Toggle):
    """Enable lore locations"""
    display_name="Lore"

@dataclass
class GrimDawnOptions(PerGameCommonOptions):
    goal: GrimDawnGoal
    forbidden_dungeons: GrimDawnForbiddenDungeons
    one_shot: GrimDawnOneShot
    secret_chest: GrimDawnSecretChest
    devotion_shrine: GrimDawnDevotionShrines
    lore: GrimDawnLore
