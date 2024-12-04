from typing import Dict

from Options import Choice, Option, Toggle, PerGameCommonOptions,DeathLink
from dataclasses import dataclass

class GrimDawnGoal(Choice):
    """
    The goal to accomplish in order to complete the seed.
    Beat Warden - Find the Warden's Lab and defeat Warden Krieg
    Beat Korvaak - Find the Tomb of the Eldritch Sun and defeat Korvaak (requires Forgotten Gods DLC)
    Beat Ravna - Find the Royal Hive under the Infested Croplands and defeat Swarm Queen Ravna
    Beat Loghorrean - Find the Tomb of the Watchers under the Necropolis and defeat The Loghorrean
    Beat Master of Flesh - Find the Fleshworks in the ruined city defeat the Master of Flesh
    """
    display_name = "Goal"

    option_beat_warden = 0
    option_beat_korvaak = 1
    option_beat_ravna = 2
    option_beat_loghorrean = 3
    option_beat_master_of_flesh = 4

    default = 0

class GrimDawnForbiddenDungeons(Toggle):
    """Enable Forbidden Dungeons and Skeleton Keys as locations"""
    display_name="Forbidden Dungeons and Skeleton Keys"

class GrimDawnOneShot(Toggle):
    """Enable One Shot Chests as locations"""
    display_name="One Shot Chests"

class GrimDawnFactionQuests(Toggle):
    """Enable Faction Quests as locations"""
    display_name="Faction Quests"

class GrimDawnSecretChest(Toggle):
    """Enable Secret Chests as locations"""
    display_name="Secret Chests"

class GrimDawnDevotionShrines(Toggle):
    """Enable Devotion Shrines as locations"""
    display_name="Devotion Shrines"

class GrimDawnLore(Toggle):
    """Enable Lore Note locations"""
    display_name="Lore"

class GrimDawnFGDLC(Toggle):
    """Enable locations inside the Forgotten Gods DLC (required for Korvaak goal)"""
    display_name="DLC: FG"

class GrimDawnSkillBalance(Toggle):
    """Randomize all numerical values in player class skills and passives, including but not limited to
    damage values, action speeds, mana costs, cooldown times, projectile count, and pet summons."""
    display_name="Skill Balance Randomizer"

class GrimDawnSBRange(Choice):
    """
    The range which skill balance randomizer can affect skill values. Has no effect if Skill Balance Randomizer is disabled.
    micro - Random range between 0.9x and 1.1x
    small - Random range between 0.75x and 1.25x
    medium - Random range between 0.66x and 1.5x
    large - Random range between 0.5x and 2x
    extreme - Random range between 0.2x and 3x
    mayhem - Random range between 0.1x and 10x. This is just for fun as this setting completely breaks game balance.
    """
    display_name = "Skill Balance Range"

    option_micro = 0
    option_small = 1
    option_medium = 2
    option_large = 3
    option_extreme = 4
    option_mayhem = 5

    default = 2
    lookupdict = {"micro":((9/10),(11/10)),"small":((3/4),(5/4)),"medium":((2/3),(3/2)),"large":((1/2),2),"extreme":((1/5),3),"mayhem":(1/100,10)}

    @property
    def lowerbound(self):
        return self.lookupdict[self.current_key][0]
    @property
    def upperbound(self):
        return self.lookupdict[self.current_key][1]

class GrimDawnSBWeight(Choice):
    """
    The weight that affects a skill's randomized value to be buffed or nerfed. Has no effect if Skill Balance Randomizer is disabled.
    only_nerfs - 100% chance for values to roll a nerf
    mostly_nerfs - 75% chance for values to roll a nerf
    balanced - 50/50 chance for values to roll a buff or nerf
    mostly_buffs - 75% chance for values to roll a buff
    only_buffs - 100% chance for values to roll a buff
    """
    display_name = "Skill Balance Weight"

    option_only_nerfs = 0
    option_mostly_nerfs = 1
    option_balanced = 2
    option_mostly_buffs = 3
    option_only_buffs = 4
    
    default = 2

@dataclass
class GrimDawnOptions(PerGameCommonOptions):
    goal: GrimDawnGoal
    forbidden_dungeons: GrimDawnForbiddenDungeons
    one_shot: GrimDawnOneShot
    secret_chest: GrimDawnSecretChest
    devotion_shrine: GrimDawnDevotionShrines
    lore: GrimDawnLore
    faction: GrimDawnFactionQuests
    dlc_fg: GrimDawnFGDLC
    skill_balance_rando: GrimDawnSkillBalance
    skill_balance_range: GrimDawnSBRange
    skill_balance_weight: GrimDawnSBWeight
    death_link: DeathLink
