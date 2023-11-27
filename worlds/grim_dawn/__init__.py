from typing import List

from BaseClasses import Region, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .Items import GrimDawnItem, item_data_table, item_table
from .Locations import GrimDawnLocation, location_data_table, location_table, locked_locations
from .Options import grim_dawn_options
from .Regions import region_data_table
from .Rules import GrimDawnRules


class GrimDawnWebWorld(WebWorld):
    theme = "partyTime"



class CliqueWorld(World):
    """It's Grim Dawn"""

    game = "Grim Dawn"
    data_version = 3
    web = GrimDawnWebWorld()
    option_definitions = grim_dawn_options
    location_name_to_id = location_table
    item_name_to_id = item_table

    def create_item(self, name: str) -> GrimDawnItem:
        return GrimDawnItem(name, item_data_table[name].type, item_data_table[name].code, self.player)
    
    def create_filler_item(self) -> GrimDawnItem:
        return GrimDawnItem(self.get_filler_item_name(), ItemClassification.filler, item_data_table[self.get_filler_item_name()].code,self.player)

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
        return "Iron Bits"

    def set_rules(self) -> None:
        grimDawnRules = GrimDawnRules(self)
        grimDawnRules.set_grim_dawn_rules()
        self.multiworld.completion_condition[self.player] = lambda state: grimDawnRules.has_scrap(state,6)

    def fill_slot_data(self):
        return None