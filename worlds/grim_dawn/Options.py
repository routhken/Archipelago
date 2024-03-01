from typing import Dict

from Options import Choice, Option, Toggle, PerGameCommonOptions,DeathLink
from dataclasses import dataclass

class GrimDawnGoal(Choice):
    """
    The goal to accomplish in order to complete the seed.
    Beat Warden - Fight your way to the warden lab and kill Warden Krieg
    Beat Ravna - Fight your way to the homestead and kill Swarm Queen Ravna
    Beat Loghorrean - Fight your way to the necropolis and kill The Loghorrean
    Beat the Master of Flesh - Fight through the Ashes of Malmoth DLC and kill the Master of Flesh
    """
    display_name = "Goal"

    option_beat_warden = 0
    option_beat_ravna = 1
    option_beat_loghorrean = 2
    option_beat_master_of_flesh = 3

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

class GrimDawnAoMDLC(Toggle):
    """Enable locations inside the AoM DLC (required for Master of Flesh goal)"""
    display_name="DLC: AoM"

@dataclass
class GrimDawnOptions(PerGameCommonOptions):
    goal: GrimDawnGoal
    forbidden_dungeons: GrimDawnForbiddenDungeons
    one_shot: GrimDawnOneShot
    secret_chest: GrimDawnSecretChest
    devotion_shrine: GrimDawnDevotionShrines
    lore: GrimDawnLore
    dlc_aom: GrimDawnAoMDLC
    death_link: DeathLink
