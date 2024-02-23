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
            "Act 1 -> Devil's Aquifer": lambda state:
                self.has_scrap(state,5),
            "Act 1 -> Sunken Reliquary": lambda state:
                state.has("Flooded Passage Destroy Blockade",self.player),
            "Act 1 -> East Marsh": lambda state:
                state.has("East Marsh Bridge Repair",self.player),
            "Act 1 -> Warden's Cellar": lambda state:
                state.has("Cellar Door Unlock",self.player),
            "Act 1 -> Act 2": lambda state:
                state.has("Arkovia Bridge Repair",self.player),

            "Act 2 -> Act 3": lambda state:
                state.has("Arkovian Foothills Destroy Barricade",self.player),

            "Act 3 -> Four Hills Secret": lambda state:
                state.has("New Harbor Destroy Barricade",self.player),
            "Act 3 -> Tyrant's Hold": lambda state:
                state.has("Prospector's Trail Destroy Barricade",self.player) or state.has("Twin Falls Bridge Repair",self.player),
            "Act 3 -> Port Valbury": lambda state:
                state.has_all(["Conflagration Destroy Barricade","Forbidden Dor Unlock"],self.player),
            "Act 3 -> Homestead Side Doors": lambda state:
                state.has("Homestead Side Doors Unlock",self.player),
            "Act 3 -> Act 4": lambda state:
                state.has("Homestead Main Doors Unlock",self.player),
            "Act 3 -> Steps of Torment": lambda state:
                state.has("Forbidden Dor Unlock", self.player),
            
            "Homestead Side Doors -> Royal Hive": lambda state:
                state.has("Royal Hive Queen Door Unlock",self.player),
            
            "East Marsh -> Temple of the Three": lambda state:
                state.has("Witch Gods Temple Unlock",self.player),

            "Act 4 -> Act 5": lambda state:
                state.has_all(["Fort Ikon Gate Unlock"],self.player),

            "Act 5 -> Act 6": lambda state:
                state.has("Fort Ikon Destroy Blockade",self.player),

            "Act 6 -> Bastion of Chaos": lambda state:
                state.has_all(["Necropolis Bridge Repair","Forbidden Dor Unlock"],self.player),
            "Act 6 -> Tomb of the Watchers": lambda state:
                state.has("Tomb of the Watchers Door Unlock",self.player),

            "Tomb of the Watchers -> Edge of Madness": lambda state:
                state.has("Loghorrean Seal Unlock",self.player),
            
            "Act 5 -> Act 7": lambda state:
                state.has("Gloomwald Destroy Blockade",self.player),
            
            "Act 7 -> Nane's Hideout": lambda state:
                state.has("Nane's Hideout Destroy Barricade",self.player),
            "Act 7 -> Ancient Grove": lambda state:
                state.has("Forbidden Dor Unlock",self.player),
            "Act 7 -> Forlorn Cellar": lambda state:
                state.has("Forlorn Cellar Unlock",self.player),
            "Act 7 -> Den of the Ancient": lambda state:
                state.has("Ugdenbog Destroy Barricade",self.player),
            "Act 7 -> Act 8": lambda state:
                state.has("Altar of Rattosh Portal",self.player),
            "Act 8 -> Candle Disctict": lambda state:
                state.has_any(["Candle District Door Unlock","Malmouth Bridge Lowered"],self.player),
            "Act 8 -> Act 9": lambda state:
                state.has("Steelcap District Door Unlock",self.player),
            
            "Act 9 -> Harbor Stash": lambda state:
                state.has("Malmouth Harbor Destroy Barricade",self.player),
            "Act 9 -> Crown Hill": lambda state:
                state.has("Crown Hill Destroy Gates",self.player),
            "Crown Hill -> Fleshworks": lambda state:
                state.has("Crown Hill Open Flesh Barrier",self.player),
            "Fleshworks -> Sanctum of Flesh": lambda state:
                state.has("Fleshworks Open Flesh Barrier", self.player),

        }

        
        self.location_rules = {
            #Act 1 Locations
            "Find Elsa":                                lambda state: self.has_scrap(state,5) and state.has("Warden's Cellar Unlock",self.player),
            "Trapped and Alone":                        lambda state: state.has("Rotting Croplands Destroy South Blockade",self.player),
            "Rashalga, the Mad Queen":                  lambda state: state.has("Lower Crossing Destroy Blockade",self.player),
            "The Hidden Path":                          lambda state: state.has_all(["Lower Crossing Destroy Blockade","Arkovia Bridge Repair","Arkovian Foothills Destroy Barricade","Homestead Main Doors Unlock","Homestead Side Doors Unlock"],self.player),
            "Rescue Garett Torvan":                     lambda state: state.has_all(["Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock"],self.player),
            "Depraved Sanctuary Exalted Stash":         lambda state: state.has("Strange Key", self.player),
            "Rotting Croplands Exalted Stash":          lambda state: state.has("Rotting Croplands Destroy North Blockade",self.player),
            "Prison Dungeons Secret Chest":             lambda state: self.has_scrap(state,5),
            "The Hidden Path - Dreeg":                  lambda state: state.has("Lower Crossing Destroy Blockade",self.player),
            "The Hidden Path - Bysmiel":                lambda state: state.has("Lower Crossing Destroy Blockade",self.player),
            "The Hidden Path - Bysmiel":                lambda state: state.has("Lower Crossing Destroy Blockade",self.player),
            "The Hidden Path - Solael":                 lambda state: state.has("Lower Crossing Destroy Blockade",self.player),
            "Journal of Inquisitor Creed - 9th Entry":  lambda state: state.has("Cellar Door Unlock",self.player),
            "Old Grove Secret Chest":                   lambda state: state.has("Old Grove Repair Bridge",self.player),

        }

    def has_scrap(self,state,q) -> bool:
        return (state.count("5 Scrap",self.player)*5) >= q

    def set_grim_dawn_rules(self) -> None:
        multiworld = self.world.multiworld


        for region in multiworld.get_regions(self.player):
            for entrance in region.entrances:
                if entrance.name in self.region_rules:
                    set_rule(entrance, self.region_rules[entrance.name])
            for location in region.locations:
                if location.name in self.location_rules:
                    set_rule(location, self.location_rules[location.name])
