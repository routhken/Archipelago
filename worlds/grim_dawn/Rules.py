from typing import Callable


from typing import Dict, Set, Callable, TYPE_CHECKING
from BaseClasses import CollectionState, MultiWorld

from worlds.generic.Rules import set_rule, add_rule

if TYPE_CHECKING:
    from . import GrimDawnWorld
else:
    GrimDawnWorld = object

class GrimDawnRules:
    world: GrimDawnWorld
    player: int
    region_rules: Dict[str, Callable[[CollectionState], bool]]

    location_rules: Dict[str, Callable[[CollectionState], bool]]

    def __init__(self, world: GrimDawnWorld) -> None:
        self.world = world
        self.player = world.player

        self.region_rules = {
            "Act 1 -> Flooded Passage Blockade": lambda state:
                state.has("Flooded Passage Destroy Blockade",self.player),
            "Act 1 -> Warden's Cellar": lambda state:
                state.has("Warden's Cellar Door",self.player),
            "Act 1 -> East Marsh Bridge": lambda state:
                state.has("East Marsh Bridge Repair",self.player),

        }

        
        self.location_rules = {
            "Repair Waterpump": lambda state:
                self.has_scrap(state,5),
            "Cleanse Slith Infestation": lambda state:
                self.has_scrap(state,5),
            "A Cultist in the Midst": lambda state:
                self.has_cultist_orders(state),
            "Depraved Sanctuary Exalted Stash": lambda state:
                self.has_strange_key(state),
            "Devotion Shrine - Devil's Aquifer": lambda state:
                self.has_scrap(state,5),
            "The Hidden Path - Dreeg": lambda state:
                state.has("Lower Crossing Destroy Blockade",self.player),

        }

    def has_cultist_orders(self, state) -> bool:
        return state.has("Cultist Orders", self.player)
    def has_strange_key(self, state) -> bool:
        return state.has("Strange Key", self.player)
    def has_scrap(self,state,q) -> bool:
        return state.count("Scrap",self.player) >= q
    def has_dynamite(self,state,q) -> bool:
        return state.count("Dynamite",self.player) >= q

    def set_grim_dawn_rules(self) -> None:
        multiworld = self.world.multiworld


        for region in multiworld.get_regions(self.player):
            for entrance in region.entrances:
                if entrance.name in self.region_rules:
                    set_rule(entrance, self.region_rules[entrance.name])
            for location in region.locations:
                if location.name in self.location_rules:
                    set_rule(location, self.location_rules[location.name])
