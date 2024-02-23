from typing import List, Any, Dict

from BaseClasses import Region, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .Items import GrimDawnItem, item_data_table, item_table,get_unique_relic,filler_table,filler_weights
from .Locations import GrimDawnLocation, location_data_table, location_table, locked_locations
from .Options import GrimDawnOptions
from .Regions import region_data_table
from .Rules import GrimDawnRules


class GrimDawnWebWorld(WebWorld):
    theme = "partyTime"



class GrimDawnWorld(World):
    """It's Grim Dawn"""

    game = "Grim Dawn"
    data_version = 3
    web = GrimDawnWebWorld()
    options_dataclass = GrimDawnOptions
    options: GrimDawnOptions
    location_name_to_id = location_table
    item_name_to_id = item_table

    def create_item(self, name: str) -> GrimDawnItem:
        return GrimDawnItem(name, item_data_table[name].type, item_data_table[name].code, self.player)
    
    def create_filler_item(self) -> GrimDawnItem:
        name = self.get_filler_item_name()
        return GrimDawnItem(name, item_data_table[name].type, item_data_table[name].code,self.player)
    
    def generate_early(self) -> None:
        if self.options.dlc_aom != 1 and self.options.goal == 3:
            raise Exception(f"[Grim Dawn - '{self.multiworld.get_player_name(self.player)}'] Goal selection is invalid without DLC: AoM enabled")

    def create_items(self) -> None:
        item_pool: List[GrimDawnItem] = []
        for name, item in item_data_table.items():
            if item.code and item.can_create(self.multiworld, self.player):
                for i in range(item.quantity):
                    item_pool.append(self.create_item(name)) #create item.quantity items by default

        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        # Fill any empty locations with filler items.
        while len(item_pool) < total_locations:
            item_pool.append(self.create_filler_item())

        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_locations({
                location_name: location_data.address for location_name, location_data in location_data_table.items()
                if location_data.region == region_name and location_data.can_create(self.multiworld, self.player)
            }, GrimDawnLocation)
            region.add_exits(region_data.connecting_regions)

        # Place locked locations.
        for location_name, location_data in locked_locations.items():
            # Ignore locations we never created.
            if not location_data.can_create(self.multiworld, self.player):
                continue
        
            locked_item = self.create_item(location_data.locked_item)
            self.multiworld.get_location(location_name, self.player).place_locked_item(locked_item)

    def get_filler_item_name(self) -> str:
        filler_name = self.multiworld.per_slot_randoms[self.player].choices(filler_table, weights=filler_weights).pop()
        if filler_name == "Relic":
            filler_name = get_unique_relic(self.multiworld.per_slot_randoms[self.player])
            if filler_name == "":
                return "Extra EXP"
        return filler_name

    def set_rules(self) -> None:
        grimDawnRules = GrimDawnRules(self)
        grimDawnRules.set_grim_dawn_rules()
        if self.multiworld.worlds[self.player].options.goal.value == 0:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Warden Boss Door Unlock",self.player)
        elif self.multiworld.worlds[self.player].options.goal.value == 1:
            self.multiworld.completion_condition[self.player] = lambda state: state.has_all(["Royal Hive Queen Door Unlock","Homestead Side Doors Unlock","Arkovian Foothills Destroy Barricade","Arkovia Bridge Repair"],self.player)
        elif self.multiworld.worlds[self.player].options.goal.value == 2:
            self.multiworld.completion_condition[self.player] = lambda state: state.has_all(["Loghorrean Seal Unlock","Tomb of the Watchers Door Unlock","Fort Ikon Destroy Blockade","Fort Ikon Gate Unlock","Homestead Main Doors Unlock","Arkovian Foothills Destroy Barricade","Arkovia Bridge Repair"],self.player)
        elif self.multiworld.worlds[self.player].options.goal.value == 3:
            self.multiworld.completion_condition[self.player] = lambda state: state.has_all(["Crown Hill Destroy Gates","Crown Hill Open Flesh Barrier","Fleshworks Open Flesh Barrier","Candle District Door Unlock","Altar of Rattosh Portal","Burrwitch Destroy Blockade"],self.player)

    def fill_slot_data(self) -> Dict[str,Any]:
        dReturn = {
            "goal":self.options.goal.value,
            "deathlink":self.options.death_link.value
        }

        return dReturn