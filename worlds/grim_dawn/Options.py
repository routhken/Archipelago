from typing import Dict

from Options import Choice, Option, Toggle, PerGameCommonOptions
from dataclasses import dataclass


class DevotionShrines(Toggle):
    """Enable Devotion Shrines as locations"""
    display_name="Devotion Shrines"

class Lore(Toggle):
    """Enable lore locations"""
    display_name="Lore"

@dataclass
class GrimDawnOptions(PerGameCommonOptions):
    devotion_shrines: DevotionShrines
    lore: Lore
