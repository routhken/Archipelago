from typing import List, Any, Dict, ClassVar
from settings import Group, FolderPath
from BaseClasses import Region, ItemClassification, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import GrimDawnItem, item_data_table, item_table,get_unique_relic,filler_table,filler_weights,relic_table
from .Locations import GrimDawnLocation, location_data_table, location_table, locked_locations
from .Options import GrimDawnOptions
from .Regions import region_data_table
from .Rules import GrimDawnRules
from .SkillRandomizer import generateSkillShuffleTable, generateSkillPatchTable, generateDevotionPatchTable
from .EnemyRandomizer import generateEnemyTable
from logging import warning
from Options import OptionError
from worlds.LauncherComponents import (
    Component,
    components,
    Type,
    launch_subprocess,
    icon_paths,
)
import json

#release version 0.3.1

class GrimDawnSettings(Group):
    class Grim_Dawn_Install_Path(FolderPath):
        """Path to Grim Dawn install directory"""
        required = True
    grimDawnInstallPath: Grim_Dawn_Install_Path = Grim_Dawn_Install_Path("")

    class Poptracker_Pack_Path(FolderPath):
        """Path to Grim Dawn poptracker pack"""
        required = False
    grimDawnPoptrackerPackPath: Poptracker_Pack_Path = Poptracker_Pack_Path("")

class GrimDawnWebWorld(WebWorld):
    theme = "partyTime"
    tutorials = [Tutorial(
        "Mod Setup and Use Guide",
        "A guide to installing AP Grim Dawn",
        "English",
        "guide_en.md",
        "setup/en",
        ["DaKennyMan","Faris"]
    )]

def launch_client(*args):
    from .GrimDawnClient import launch
    launch_subprocess(launch, name="GrimDawnClient", args=args)


icon_paths["GDLogo"] = f"ap:{__name__}/GDLogo.png"

components.append(Component(
    "Grim Dawn Client",
    func=launch_client,
    component_type=Type.CLIENT,
    icon = "GDLogo",
    supports_uri = True,
    game_name = "Grim Dawn"
    ))

class GrimDawnWorld(World):
    """It's Grim Dawn"""

    game = "Grim Dawn"
    web = GrimDawnWebWorld()
    options_dataclass = GrimDawnOptions
    options: GrimDawnOptions
    location_name_to_id = location_table
    item_name_to_id = item_table
    local_relic_table: List[str]
    settings: ClassVar[GrimDawnSettings]
    skill_balance_table: Dict[str, Dict[str, Dict[str, any]]]
    tracker_world = {"external_pack_key": "grimDawnPoptrackerPackPath", "map_page_maps": "maps/maps.json", "map_page_locations": "locations/locations.json"}
    glitches_item_name = "outOfLogicItem"

    def create_item(self, name: str) -> GrimDawnItem:
        if name == self.glitches_item_name:
            return GrimDawnItem(self.glitches_item_name, ItemClassification.progression, None, self.player)
        return GrimDawnItem(name, item_data_table[name].type, item_data_table[name].code, self.player)
    
    def generate_early(self) -> None:
        self.local_relic_table = relic_table.copy()
        self.random.shuffle(self.local_relic_table) #only need to shuffle this once per world
        if (not self.options.dlc_fg) and self.options.goal == 1:
            raise OptionError(f"[Grim Dawn - '{self.multiworld.get_player_name(self.player)}'] Goal selection is invalid without DLC: FG enabled.")
        if (not self.options.dlc_aom) and self.options.goal == 4:
            raise OptionError(f"[Grim Dawn - '{self.multiworld.get_player_name(self.player)}'] Goal selection is invalid without DLC: AoM enabled.")
        if ((not self.options.dlc_fg) or (not self.options.dlc_aom)) and self.options.goal == 50:
            raise OptionError(f"[Grim Dawn - '{self.multiworld.get_player_name(self.player)}'] Goal selection is invalid without both DLC: AoM and DLC: FG enabled.")

    def create_items(self) -> None:
        item_pool: List[GrimDawnItem] = []
        for name, item in item_data_table.items():
            if item.code and item.can_create(self):
                for i in range(item.quantity):
                    item_pool.append(self.create_item(name)) #create item.quantity items by default

        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        if self.options.progressive_progression == True:
            # Create generic progression items to replace the named ones
            main_quantity = 0
            fg_quantity = 1
            aom_quantity = 0

            if (self.options.goal == "beat_warden") or (self.options.goal == "beat_korvaak"):
                pass
            elif self.options.goal == "beat_ravna":
                main_quantity = 2
            elif self.options.goal == "beat_loghorrean":
                main_quantity = 7
            else:
                main_quantity = 7
            
            if (self.options.dlc_aom == True) and ((self.options.goal == "beat_master_of_flesh") or (self.options.goal == "beat_all_bosses") or (self.options.goal == "emblem_hunt")):
                aom_quantity = 6
            
            if (self.options.dlc_fg == True) and (self.options.goal != "beat_warden"):
                fg_quantity = 4

            for _ in range(main_quantity):
                item_pool.append(self.create_item("Progressive Main Campaign"))
            for _ in range(fg_quantity):
                item_pool.append(self.create_item("Progressive Forgotten Gods"))
            for _ in range(aom_quantity):
                item_pool.append(self.create_item("Progressive Ashes of Malmouth"))

        if self.options.goal == "emblem_hunt":
            # Handle having more max emblems than total filler space available
            max_filler_space = total_locations - len(item_pool)
            if self.options.max_emblems > max_filler_space:
                self.options.max_emblems.value = max_filler_space
                warning(f"Max emblems desired was higher than available filler space, reduced max emblem count to {max_filler_space}.")
            # Handle having more emblems required than max emblems available
            if self.options.required_emblems > self.options.max_emblems:
                self.options.required_emblems.value = self.options.max_emblems.value
                warning(f"Required emblems was higher than max emblems, reduced required emblems to match max emblem count of {self.options.required_emblems.value}.")
            # Create emblems
            for _ in range(self.options.max_emblems.value):
                item_pool.append(self.create_item("Aetherial Emblem"))

        # Fill a specified amount of empty locations with trap items.
        amountOfTraps = ((total_locations - len(item_pool)) * self.options.trap_percent) // 100
        for _ in range(amountOfTraps):
            item_pool.append(self.create_trap())

        # Fill any empty locations with filler items.
        while len(item_pool) < total_locations:
            item_pool.append(self.create_filler())

        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        # Create regions.
        skipped_regions = []
        for region_name, region_data in region_data_table.items():
            if region_data.can_create(self.multiworld, self.player):
                region = Region(region_name, self.player, self.multiworld)
                self.multiworld.regions.append(region)
            else:
                skipped_regions.append(region_name)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            if region_data.can_create(self.multiworld, self.player):
                region = self.multiworld.get_region(region_name, self.player)
                region.add_locations({
                    location_name: location_data.address for location_name, location_data in location_data_table.items()
                    if location_data.region == region_name and location_data.can_create(self)
                }, GrimDawnLocation)
                region.add_exits([item for item in region_data.connecting_regions if item not in skipped_regions])

        # Place locked locations.
        for location_name, location_data in locked_locations.items():
            # Ignore locations we never created.
            if not location_data.can_create(self.multiworld, self.player):
                continue
        
            locked_item = self.create_item(location_data.locked_item)
            self.multiworld.get_location(location_name, self.player).place_locked_item(locked_item)

    def create_trap(self):
        name = self.random.choices(list(self.options.trap_weights.keys()), weights = list(self.options.trap_weights.values())).pop()
        return self.create_item(name)

    def get_filler_item_name(self) -> str:
        filler_name = self.random.choices(filler_table, weights=filler_weights).pop()
        if filler_name == "Relic":
            filler_name = get_unique_relic(self)
            if filler_name == "":
                return "Extra EXP"
        return filler_name

    def set_rules(self) -> None:
        grimDawnRules = GrimDawnRules(self)
        grimDawnRules.set_grim_dawn_rules()
        if self.options.goal == "beat_warden":
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("Warden Krieg","Location",self.player)#.has("Warden Boss Door Unlock",self.player)
        elif self.options.goal == "beat_korvaak":
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("Manifestation of Korvaak, the Eldritch Sun","Location",self.player)
        elif self.options.goal == "beat_ravna":
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("Swarm Queen Ravna","Location",self.player)#.has_all(["Royal Hive Queen Door Unlock","Homestead Side Doors Unlock","Arkovian Foothills Destroy Barricade","Arkovia Bridge Repair"],self.player)
        elif self.options.goal == "beat_loghorrean":
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("The Loghorrean","Location",self.player)#.has_all(["Loghorrean Seal Unlock","Tomb of the Watchers Door Unlock","Fort Ikon Destroy Blockade","Fort Ikon Gate Unlock","Homestead Main Doors Unlock","Arkovian Foothills Destroy Barricade","Arkovia Bridge Repair"],self.player)
        elif self.options.goal == "beat_master_of_flesh":
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach("Master of Flesh","Location",self.player)#  .has_all(["Crown Hill Destroy Gates","Crown Hill Open Flesh Barrier","Fleshworks Open Flesh Barrier","Candle District Door Unlock","Altar of Rattosh Portal","Gloomwald Destroy Blockade"],self.player)
        elif self.options.goal == "beat_all_bosses":
            self.multiworld.completion_condition[self.player] = lambda state: (state.can_reach("Master of Flesh","Location",self.player) and state.can_reach("The Loghorrean","Location",self.player) and state.can_reach("Swarm Queen Ravna","Location",self.player) and state.can_reach("Manifestation of Korvaak, the Eldritch Sun","Location",self.player) and state.can_reach("Warden Krieg","Location",self.player))
        elif self.options.goal == "emblem_hunt":
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Aetherial Emblem",self.player,self.options.required_emblems.value)

    # When getting progressive progression, this function checks for special interaction
    def collect_item(self,state,item,remove = False) -> str | None:
        def handle_list(prog_items):
            if not remove:
                for next_item in prog_items:
                    if not state.has(next_item, self.player):
                        return next_item
            else:
                for next_item in reversed(prog_items):
                    if state.has(next_item, self.player):
                        return next_item

        prog_main = ["Arkovia Bridge Repair", "Arkovian Foothills Destroy Barricade", "Homestead Main Doors Unlock", "Fort Ikon Gate Unlock", "Fort Ikon Destroy Blockade", "Tomb of the Watchers Door Unlock", "Loghorrean Seal Unlock"]
        prog_aom = ["Gloomwald Destroy Blockade", "Altar of Rattosh Portal", "Steelcap District Door Unlock", "Crown Hill Destroy Gates", "Crown Hill Open Flesh Barrier", "Fleshworks Open Flesh Barrier"]
        prog_fg = ["Warden Boss Door Unlock", "Vanguard of the Three Door Unlock", "Path of Ascension Destroy Barrier", "Eldritch Gate Destroy Barrier"]

        if item.name == "Progressive Main Campaign":
            return handle_list(prog_main)
        elif item.name == "Progressive Forgotten Gods":
            return handle_list(prog_fg)
        elif item.name == "Progressive Ashes of Malmouth":
            return handle_list(prog_aom)
        return super().collect_item(state,item,remove)

    def write_spoiler(self, spoiler_handle):
        spoiler_handle.write("\nSkill Shuffle Table for player " + self.player_name + ":\n")
        spoiler_handle.write(json.dumps(self.skill_shuffle_table, indent=4))
        spoiler_handle.write("\nSkill Balance Table for player " + self.player_name + ":\n")
        spoiler_handle.write(json.dumps(self.skill_balance_table, indent=4))
        spoiler_handle.write("\nDevotion Balance Table for player " + self.player_name + ":\n")
        spoiler_handle.write(json.dumps(self.devotion_balance_table, indent=4))
        spoiler_handle.write("\nEnemy Table for player " + self.player_name + ":\n")
        spoiler_handle.write(json.dumps(self.enemy_table, indent=4))

    def generate_basic(self) -> None:
        if not self.options.skill_shuffler:
            self.skill_shuffle_table = {}
        else:
            self.skill_shuffle_table = generateSkillShuffleTable(self)
        if not self.options.skill_balance_randomizer:
            self.skill_balance_table = {}
        else:
            self.skill_balance_table = generateSkillPatchTable(self)
        if not self.options.devotion_balance_randomizer:
            self.devotion_balance_table = {}
        else:
            self.devotion_balance_table = generateDevotionPatchTable(self)
        if not self.options.enemy_randomizer:
            self.enemy_table = []
        else:
            self.enemy_table = generateEnemyTable(self)

    def fill_slot_data(self) -> Dict[str,Any]:
        dReturn = {
            "goal":self.options.goal.value,
            "max_emblems":self.options.max_emblems.value,
            "required_emblems":self.options.required_emblems.value,
            "deathlink":self.options.death_link.value,
            "forbidden_dungeons": self.options.forbidden_dungeons.value,
            "faction": self.options.faction.value,
            "one_shot": self.options.one_shot.value,
            "secret_chest": self.options.secret_chest.value,
            "devotion_shrine": self.options.devotion_shrine.value,
            "lore": self.options.lore.value,
            "progressive_progression":self.options.progressive_progression.value,
            "dlc_aom": self.options.dlc_aom.value,
            "dlc_fg": self.options.dlc_fg.value,
            "skill_shuffler": self.options.skill_shuffler.value,
            "skill_shuffle_table": self.skill_shuffle_table,
            "skill_balance_randomizer": self.options.skill_balance_randomizer.value,
            "devotion_balance_randomizer": self.options.devotion_balance_randomizer.value,
            "skill_balance_range": self.options.skill_balance_range.value,
            "skill_balance_table": self.skill_balance_table,
            "devotion_balance_table": self.devotion_balance_table,
            "skill_balance_weight": self.options.skill_balance_weight.value,
            "skill_balance_preserve_damage": self.options.skill_balance_preserve_damage.value,
            "skill_balance_preserve_area": self.options.skill_balance_preserve_area.value,
            "skill_balance_preserve_duration": self.options.skill_balance_preserve_duration.value,
            "skill_balance_preserve_mana": self.options.skill_balance_preserve_mana.value,
            "skill_balance_preserve_projectiles": self.options.skill_balance_preserve_projectiles.value,
            "skill_balance_preserve_cooldown": self.options.skill_balance_preserve_cooldown.value,
            "skill_balance_preserve_chance": self.options.skill_balance_preserve_chance.value,
            "skill_balance_preserve_defense": self.options.skill_balance_preserve_defense.value,
            "skill_balance_preserve_summons": self.options.skill_balance_preserve_summons.value,
            "skill_balance_preserve_speed": self.options.skill_balance_preserve_speed.value,
            "starting_skill_points": self.options.starting_skill_points.value,
            "free_skill_respec": self.options.free_skill_respec.value,
            "enemy_randomizer": self.options.enemy_randomizer.value,
            "enemy_table": self.enemy_table,
            "dangerous_enemies": self.options.dangerous_enemies.value,
            "buff_enemies": self.options.buff_enemies.value,
        }

        return dReturn