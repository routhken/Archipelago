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
            "Act 1 -> Flooded Passage": lambda state:
                state.has("Flooded Passage Destroy Blockade",self.player),
            "Act 1 -> Warden's Cellar": lambda state:
                state.has("Warden's Cellar Unlock",self.player),
            "Act 1 -> East Marsh": lambda state:
                state.has("East Marsh Bridge Repair",self.player),
            "Act 1 -> Act 2": lambda state:
                state.has("Arkovia Bridge Repair",self.player),
            "Act 2 -> Act 3": lambda state:
                state.has("Arkovian Foothills Destroy Barricade",self.player),
            "Act 3 -> New Harbor": lambda state:
                state.has("New Harbor Destroy Barricade",self.player),
            "Act 3 -> Desert": lambda state:
                state.has("Prospector's Trail Destroy Barricade",self.player) or state.has("Twin Falls Bridge Repair",self.player),
            "Act 3 -> Homestead Side Doors": lambda state:
                state.has("Homestead Side Doors Unlock",self.player),
            "Act 3 -> Conflagration": lambda state:
                state.has_all(["Conflagration Destroy Barricade","Skeleton Key"],self.player),
            "Act 3 -> Act 4": lambda state:
                state.has("Homestead Main Doors Unlock",self.player),

        }

        
        self.location_rules = {
            #Act 1 Locations
            "Repair Waterpump": lambda state:
                self.has_scrap(state,5),
            "Cleanse Slith Infestation": lambda state:
                self.has_scrap(state,5),
            "Cultist in the Midst": lambda state:
                self.has_cultist_orders(state),
            "Depraved Sanctuary Exalted Stash": lambda state:
                self.has_strange_key(state),
            "Find Elsa": lambda state:
                self.has_scrap(state,5) and state.has("Warden's Cellar Unlock",self.player),
            "Rotting Croplands Exalted Stash": lambda state:
                state.has("Rotting Croplands Destroy North Blockade",self.player),
            "Trapped and Alone": lambda state:
                state.has("Rotting Croplands Destroy South Blockade",self.player),
            "Devotion Shrine - Devil's Aquifer": lambda state:
                self.has_scrap(state,5),
            "The Hidden Path - Dreeg": lambda state:
                state.has("Lower Crossing Destroy Blockade",self.player),
            "Kill Swarm Queen Ravna": lambda state:
                state.has("Royal Hive Queen Door Unlock",self.player),
            "Chamber of Souls": lambda state:
                state.has("Skeleton Key", self.player),
            "Kill Alkamos, Lord Executioner": lambda state:
                state.has("Skeleton Key", self.player),
            "Suffering West Secret Chest": lambda state:
                state.has("Skeleton Key", self.player),
            "Suffering North Secret Chest": lambda state:
                state.has("Skeleton Key", self.player),
            "Anguish Secret Chest": lambda state:
                state.has("Skeleton Key", self.player),
            "Prison Dungeons Secret Chest": lambda state:
                self.has_scrap(state,5),

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
