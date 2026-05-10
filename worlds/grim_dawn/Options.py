from typing import Dict

from Options import Choice, Range, Option, Toggle, PerGameCommonOptions,DeathLink, OptionCounter
from dataclasses import dataclass
from .Items import _item_data_list
from BaseClasses import ItemClassification

class GrimDawnGoal(Choice):
    """
    The goal to accomplish in order to complete the game.
    Beat Warden - Find the Warden's Lab and defeat Warden Krieg
    Beat Korvaak - Find the Tomb of the Eldritch Sun and defeat Korvaak (requires Forgotten Gods DLC)
    Beat Ravna - Find the Royal Hive under the Infested Croplands and defeat Swarm Queen Ravna
    Beat Loghorrean - Find the Tomb of the Watchers under the Necropolis and defeat The Loghorrean
    Beat Master of Flesh - Find the Fleshworks in the ruined city and defeat The Master of Flesh (requires Ashes of Malmouth DLC)
    Beat All Bosses - Find and defeat all of the above bosses (requires both DLC)
    Emblem Hunt - Find the Aetherial Emblems scattered throughout the multiworld
    """
    display_name = "Goal"

    option_beat_warden = 0
    option_beat_korvaak = 1
    option_beat_ravna = 2
    option_beat_loghorrean = 3
    option_beat_master_of_flesh = 4
    option_beat_all_bosses = 50
    option_emblem_hunt = 51

    default = 0

class GrimDawnMaxEmblems(Range):
    """
    Maximum number of Aetherial Emblems that will be in the item pool.
    Does nothing if the goal is not set to Emblem Hunt.
    This converts filler items into Emblems, if there is not enough filler, then the max emblem count will be reduced to match the available filler.
    """
    display_name = "Max Number of Aetherial Emblems"
    range_start = 1
    range_end = 100
    default = 50

class GrimDawnRequiredEmblems(Range):
    """
    Number of Aetherial Emblems that are required to complete the Emblem Hunt goal.
    Does nothing if the goal is not set to Emblem Hunt.
    If required emblems is higher than max emblems, then required emblems will be reduced to match max emblems.
    """
    display_name = "Required number of Aetherial Emblems"
    range_start = 1
    range_end = 100
    default = 50

class GrimDawnForbiddenDungeons(Toggle):
    """Enable Forbidden Dungeons (aka Challenge Dungeons) as locations"""
    display_name="Forbidden Dungeons"

class GrimDawnOneShot(Toggle):
    """Enable One Shot (aka Exalted) Chests as locations"""
    display_name="One Shot Chests"

class GrimDawnFactionQuests(Toggle):
    """
    Enable Faction Quests as locations
    Various enemies, lore notes, quest, etc are part of this location pool.
    Adds items to the pool that max your standing with specific factions, such as "Devil's Crossing Revered"
    """
    display_name="Faction Quests"

class GrimDawnSecretChest(Toggle):
    """Enable Secret Chests as locations"""
    display_name="Secret Chests"

class GrimDawnDevotionShrines(Toggle):
    """Enable Devotion Shrines as locations"""
    display_name="Devotion Shrines"

class GrimDawnLore(Toggle):
    """
    Enable Lore Note locations
    Does not include missable or RNG lore notes.
    """
    display_name="Lore"

class GrimDawnBlockFloodedPassage(Toggle):
    """
    If enabled, blocks the exit in Flooded Passage, spliting act 1 in two and logically requiring Wightmire Bridge Repair to proceed.
    """
    display_name="Block Flooded Passage Exit"

class GrimDawnProgressiveProgression(Toggle):
    """If enabled, will convert major progression items into generic progression items so that major progression will always be unlocked in order.
    For example, Arkovia Bridge Repair and Arkovian Foothills Barricade Destroy will be converted into two Progressive Main Campaign items
    and receiving them in any order will always unlock arkovia bridge repair first. Side areas like East Marsh will be unaffected."""
    display_name="Progressive Progression"

class GrimDawnAoMDLC(Toggle):
    """Enable locations inside the Ashes of Malmouth DLC (required for Master of Flesh goal)"""
    display_name="DLC: Ashes of Malmouth"

class GrimDawnFGDLC(Toggle):
    """Enable locations inside the Forgotten Gods DLC (required for Korvaak goal)
    Beware that Forgotten Gods also requires you to own and have installed Ashes of Malmouth, even though you can still disable Ashes of Malmouth locations with the option above."""
    display_name="DLC: Forgotten Gods"

class GrimDawnSkillShuffle(Toggle):
    """Randomize player class's skills. Player class skills are divided into groups and the skill groups are shuffled among themselves.
    Therefore active skills are shuffled amoung themselves, passive skills which reserve mana are shuffled among themselves, etc.
    There is no guaranteed usability between skills and modifiers shuffled this way, for example a modifier which increases projectile
    damage will likely have no effect on Horn of Gandarr."""
    display_name="Skill Shuffler"

class GrimDawnSkillBalance(Toggle):
    """Randomize all numerical values in player class skills and passives, including but not limited to
    damage values, action speeds, mana costs, cooldown times, projectile count, and pet summons."""
    display_name="Skill Balance Randomizer"

class GrimDawnDevotionBalance(Toggle):
    """Randomize all numerical values in player devotion skills in the constellation tree, including but not limited to
    damage values, action speeds, mana costs, cooldown times, projectile count, and pet summons.
    Only the skills are randomized, not the passive nodes leading up to them."""
    display_name="Devotion Balance Randomizer"

class GrimDawnSBRange(Choice):
    """
    The range which skill balance randomizer can affect skill values. Has no effect if Skill/Devotion Balance Randomizer is disabled.
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
    The weight that affects a skill's randomized value to be buffed or nerfed. Has no effect if Skill/Devotion Balance Randomizer is disabled.
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
    """If enabled, prevents base damage and damage multiplier values from being randomized.
    Has no effect if Skill/Devotion Balance Randomizer is disabled."""
    display_name="Skill Balance Preserve Damage"

class GrimDawnSBPreserveArea(Toggle):
    """If enabled, prevents area, distance, and target values from being randomized.
    Has no effect if Skill/Devotion Balance Randomizer is disabled."""
    display_name="Skill Balance Preserve Area"

class GrimDawnSBPreserveDuration(Toggle):
    """If enabled, prevents effect duration and summon lifetime values from being randomized.
    Has no effect if Skill/Devotion Balance Randomizer is disabled."""
    display_name="Skill Balance Preserve Duration"

class GrimDawnSBPreserveMana(Toggle):
    """If enabled, prevents mana cost and mana reservation values from being randomized.
    Has no effect if Skill/Devotion Balance Randomizer is disabled."""
    display_name="Skill Balance Preserve Mana"

class GrimDawnSBPreserveProjectile(Toggle):
    """If enabled, prevents projectile and fragment values from being randomized.
    Has no effect if Skill/Devotion Balance Randomizer is disabled."""
    display_name="Skill Balance Preserve Projectiles"

class GrimDawnSBPreserveCooldown(Toggle):
    """If enabled, prevents cooldown values from being randomized.
    Has no effect if Skill/Devotion Balance Randomizer is disabled."""
    display_name="Skill Balance Preserve Cooldown"

class GrimDawnSBPreserveChance(Toggle):
    """If enabled, prevents chance to activate effect values from being randomized.
    Has no effect if Skill/Devotion Balance Randomizer is disabled."""
    display_name="Skill Balance Preserve Chance"

class GrimDawnSBPreserveDefense(Toggle):
    """If enabled, prevents defensive values from being randomized.
    Has no effect if Skill/Devotion Balance Randomizer is disabled."""
    display_name="Skill Balance Preserve Defense"

class GrimDawnSBPreserveSummon(Toggle):
    """If enabled, prevents summon amount and summon limit values from being randomized.
    Has no effect if Skill/Devotion Balance Randomizer is disabled."""
    display_name="Skill Balance Preserve Summon"

class GrimDawnSBPreserveSpeed(Toggle):
    """If enabled, prevents attack, cast, and movement speed values from being randomized.
    Has no effect if Skill/Devotion Balance Randomizer is disabled."""
    display_name="Skill Balance Preserve Speed"

class GrimDawnPetsLiveForever(Toggle):
    """If enabled, all pets, totems and traps live a very long time.
    If skill balance rando is also enabled, this takes priority."""
    display_name="Summons Live Forever"

class GrimDawnUltraRapidFire(Toggle):
    """If enabled, all mana costs and cooldowns are reduced by 85% for players and enemies.
    If skill balance rando is also enabled, this takes priority."""
    display_name="Ultra Rapid Fire"

class GrimDawnStartingSkillPoints(Toggle):
    """If enabled, you will receive 1 level up and 3 skill points when you first connect to the multiworld."""
    display_name="Starting Skill Points"

class GrimDawnFreeSkillRespec(Toggle):
    """If enabled, makes the skill respec NPCs cost nothing."""
    display_name="Free Skill Respec"

class GrimDawnDevotionShrinesCostAether(Toggle):
    """If enabled, devotion shrines that require an offering to restore will only require aether crystals, excluding the Mogdrogen shrine."""
    display_name="Easy Shrine Offerings"

class GrimDawnEnemyRandomizer(Toggle):
    """Randomize most non-boss enemies."""
    display_name="Enemy Randomizer"

class GrimDawnEnemyDangerous(Toggle):
    """Randomizes enemies to be only dangerous enemies."""
    display_name="Dangerous Enemies"

class GrimDawnEnemyBuffs(Choice):
    """
    Increase enemy total speed, size, and add levels to their skills.
    weakest - 40% decreased action speed and size, -3 to all skills
    weaker - 15% decreased action speed and size, -1 to all skills
    none - no buffs
    stronger - 15% increased action speed and size, +1 to all skills
    strongest - 40% increased action speed and size, +3 to all skills
    """
    display_name="Buff Enemies"

    option_weakest = 0
    option_weaker = 1
    option_none = 2
    option_stronger = 3
    option_strongest = 4
    
    default = 2

class GrimDawnThirdPersonCamera(Toggle):
    """Changes the camera position to be behind you like in a 3rd person shooter/platformer."""
    display_name="Third Person Camera"

class GrimDawnGenericGearQuality(Choice):
    """
    Adjust the chance of generic gear drops to be more or less likey to have rare affixes.
    Only affects loot that rolls as a generic gear drop, does not change the odds of loot rolling as
    currency, crafting materia, epic/legendary gear, or monsters/events with scripted rare gear drops.
    Becomes more noticeable beyond level 10.
    """
    display_name="Generic Gear Quality"

    option_ruthless = 0
    option_sparse = 1
    option_unchanged = 2
    option_generous = 3
    option_luxurious = 4
    
    default = 2

# class GrimDawnHintScouts(Toggle):
#     """If enabled, certain NPCs will reveal if a region (for example Wightmire) contains a progression item or not."""
#     display_name="Hint Scouts"

class TrapPercentage(Range):
    """
    Replaces filler items with traps, at the specified rate.
    """
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 5

_default_trap_weights = {
    item_definition[0]: 10
    for item_definition in _item_data_list
    if item_definition[1] is ItemClassification.trap
}

class TrapWeights(OptionCounter):
    """
    Specify the weights determining how many copies of each trap item will be in your itempool.
    If you don't want a specific type of trap, you can set the weight for it to 0.
    """
    display_name = "Trap Weights"
    valid_keys = _default_trap_weights.keys()

    min = 0

    default = _default_trap_weights

@dataclass
class GrimDawnOptions(PerGameCommonOptions):
    goal: GrimDawnGoal
    max_emblems: GrimDawnMaxEmblems
    required_emblems: GrimDawnRequiredEmblems
    forbidden_dungeons: GrimDawnForbiddenDungeons
    one_shot: GrimDawnOneShot
    secret_chest: GrimDawnSecretChest
    devotion_shrine: GrimDawnDevotionShrines
    lore: GrimDawnLore
    block_flooded_passage: GrimDawnBlockFloodedPassage
    progressive_progression: GrimDawnProgressiveProgression
    faction: GrimDawnFactionQuests
    dlc_aom: GrimDawnAoMDLC
    dlc_fg: GrimDawnFGDLC
    skill_shuffler: GrimDawnSkillShuffle
    skill_balance_randomizer: GrimDawnSkillBalance
    devotion_balance_randomizer: GrimDawnDevotionBalance
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
    pets_forever: GrimDawnPetsLiveForever
    ultra_rapid_fire: GrimDawnUltraRapidFire
    starting_skill_points: GrimDawnStartingSkillPoints
    free_skill_respec: GrimDawnFreeSkillRespec
    easy_shrine_cost: GrimDawnDevotionShrinesCostAether
    enemy_randomizer: GrimDawnEnemyRandomizer
    dangerous_enemies: GrimDawnEnemyDangerous
    third_person_camera: GrimDawnThirdPersonCamera
    generic_gear_quality: GrimDawnGenericGearQuality
    # hint_scouts: GrimDawnHintScouts
    buff_enemies: GrimDawnEnemyBuffs
    trap_percent: TrapPercentage
    trap_weights: TrapWeights
    death_link: DeathLink
