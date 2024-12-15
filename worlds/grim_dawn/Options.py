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
    Beat Master of Flesh - Find the Fleshworks in the ruined city and defeat The Master of Flesh (requires Ashes of Malmouth DLC)
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
    lookupdict = {"micro":((9/10),(11/10)),"small":((3/4),(5/4)),"medium":((2/3),(3/2)),"large":((1/2),2),"extreme":((1/5),3),"mayhem":(1/10,10)}

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

class GrimDawnSBPreserveDamage(Toggle):
    """If enabled, prevents base damage and damage multiplier values from being randomized."""
    display_name="Skill Balance Preserve Damage"

class GrimDawnSBPreserveArea(Toggle):
    """If enabled, prevents area, distance, and target values from being randomized."""
    display_name="Skill Balance Preserve Area"

class GrimDawnSBPreserveDuration(Toggle):
    """If enabled, prevents effect duration and summon lifetime values from being randomized."""
    display_name="Skill Balance Preserve Duration"

class GrimDawnSBPreserveMana(Toggle):
    """If enabled, prevents mana cost and mana reservation values from being randomized."""
    display_name="Skill Balance Preserve Mana"

class GrimDawnSBPreserveProjectile(Toggle):
    """If enabled, prevents projectile and fragment values from being randomized."""
    display_name="Skill Balance Preserve Projectiles"

class GrimDawnSBPreserveCooldown(Toggle):
    """If enabled, prevents cooldown values from being randomized."""
    display_name="Skill Balance Preserve Cooldown"

class GrimDawnSBPreserveChance(Toggle):
    """If enabled, prevents chance to activate effect values from being randomized."""
    display_name="Skill Balance Preserve Chance"

class GrimDawnSBPreserveDefense(Toggle):
    """If enabled, prevents defensive values from being randomized."""
    display_name="Skill Balance Preserve Defense"

class GrimDawnSBPreserveSummon(Toggle):
    """If enabled, prevents summon amount and summon limit values from being randomized."""
    display_name="Skill Balance Preserve Summon"

class GrimDawnSBPreserveSpeed(Toggle):
    """If enabled, prevents attack, cast, and movement speed values from being randomized."""
    display_name="Skill Balance Preserve Speed"

class GrimDawnStartingSkillPoints(Toggle):
    """If enabled, you will receive 1 level up and 3 skill points when you first connect to the multiworld."""
    display_name="Starting Skill Points"

class GrimDawnFreeSkillRespec(Toggle):
    """If enabled, makes the skill respec NPCs cost nothing."""
    display_name="Free Skill Respec"

class GrimDawnEnemyRandomizer(Toggle):
    """COMING SOON! Randomize non-boss enemies. Usually causes the early game the be much more difficult."""
    display_name="Enemy Randomizer"

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
    skill_balance_randomizer: GrimDawnSkillBalance
    skill_balance_range: GrimDawnSBRange
    skill_balance_weight: GrimDawnSBWeight
    skill_balance_preserve_damage: GrimDawnSBPreserveDamage
    skill_balance_preserve_area: GrimDawnSBPreserveArea
    skill_balance_preserve_duration: GrimDawnSBPreserveDuration
    skill_balance_preserve_mana: GrimDawnSBPreserveMana
    skill_balance_preserve_projectiles: GrimDawnSBPreserveProjectile
    skill_balance_preserve_cooldown: GrimDawnSBPreserveCooldown
    skill_balance_preserve_chance: GrimDawnSBPreserveChance
    skill_balance_preserve_defense: GrimDawnSBPreserveDefense
    skill_balance_preserve_summons: GrimDawnSBPreserveSummon
    skill_balance_preserve_speed: GrimDawnSBPreserveSpeed
    starting_skill_points: GrimDawnStartingSkillPoints
    free_skill_respec: GrimDawnFreeSkillRespec
    enemy_randomizer: GrimDawnEnemyRandomizer
    death_link: DeathLink
