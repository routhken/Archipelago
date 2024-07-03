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
                state.has("Warden Boss Door Unlock",self.player),
            "Act 1 -> Act 2": lambda state:
                state.has("Arkovia Bridge Repair",self.player),

            "Act 2 -> Act 3": lambda state:
                state.has("Arkovian Foothills Destroy Barricade",self.player),

            "Act 3 -> Four Hills Secret": lambda state:
                state.has("New Harbor Destroy Barricade",self.player),
            "Act 3 -> Tyrant's Hold": lambda state:
                state.has("Prospector's Trail Destroy Barricade",self.player) or state.has("Twin Falls Bridge Repair",self.player),
            "Act 3 -> Port Valbury": lambda state:
                state.has_all(["Conflagration Destroy Barricade","Forbidden Door Unlock"],self.player),
            "Act 3 -> Homestead Side Doors": lambda state:
                state.has("Homestead Side Doors Unlock",self.player),
            "Act 3 -> Act 4": lambda state:
                state.has("Homestead Main Doors Unlock",self.player),
            "Act 3 -> Steps of Torment": lambda state:
                state.has("Forbidden Door Unlock", self.player),
            "Act 3 -> Act 7": lambda state:
                state.has("Gloomwald Destroy Blockade",self.player),
            
            "Homestead Side Doors -> Royal Hive": lambda state:
                state.has("Royal Hive Queen Door Unlock",self.player),
            
            "East Marsh -> Temple of the Three": lambda state:
                state.has("Witch Gods Temple Unlock",self.player),

            "Act 4 -> Act 5": lambda state:
                state.has_all(["Fort Ikon Gate Unlock"],self.player),

            "Act 5 -> Act 6": lambda state:
                state.has("Fort Ikon Destroy Blockade",self.player),

            "Act 6 -> Bastion of Chaos": lambda state:
                state.has_all(["Necropolis Bridge Repair","Forbidden Door Unlock"],self.player),
            "Act 6 -> Tomb of the Watchers": lambda state:
                state.has("Tomb of the Watchers Door Unlock",self.player),

            "Tomb of the Watchers -> Edge of Madness": lambda state:
                state.has("Loghorrean Seal Unlock",self.player),
            
            
            "Act 7 -> Nane's Hideout": lambda state:
                state.has("Nane's Hideout Destroy Barricade",self.player),
            "Act 7 -> Ancient Grove": lambda state:
                state.has("Forbidden Door Unlock",self.player),
            "Act 7 -> Forlorn Cellar": lambda state:
                state.has("Forlorn Cellar Unlock",self.player),
            "Act 7 -> Den of the Ancient": lambda state:
                state.has("Ugdenbog Destroy Barricade",self.player),
            "Act 7 -> Act 8": lambda state:
                state.has("Altar of Rattosh Portal",self.player),
            "Act 8 -> Candle Disctict": lambda state:
                state.has("Candle District Door Unlock",self.player),
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
            "Act 10 -> Act 11": lambda state:
                state.has("Vanguard of the Three Door Unlock",self.player),
            "Act 11 -> Lost Oasis": lambda state:
                state.has("Valley of the Chosen Destroy Barrier",self.player),
            "Act 11 -> Tomb of the Eldritch Sun": lambda state:
                state.has("Path of Ascension Destroy Barrier", self.player),
            "Tomb of the Eldritch Sun -> The Eldritch Gate": lambda state:
                state.has("Eldritch Gate Destroy Barrier", self.player),

        }

        
        self.location_rules = {
            #Act 1 Locations
            "Find Elsa":                                        lambda state: self.has_scrap(state,5) and state.has("Warden Boss Door Unlock",self.player),
            "Trapped and Alone":                                lambda state: state.has("Rotting Croplands Destroy South Blockade",self.player),
            "Rashalga, the Mad Queen":                          lambda state: state.has("Lower Crossing Destroy Blockade",self.player),
            "The Hidden Path":                                  lambda state: state.has_all(["Lower Crossing Destroy Blockade","Arkovia Bridge Repair","Arkovian Foothills Destroy Barricade","Homestead Main Doors Unlock"],self.player),
            "Rescue Garett Torvan":                             lambda state: state.has_all(["Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Convince Ulgrim":                                  lambda state: state.has_all(["Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Steelcap District Riftgate Secured":               lambda state: state.has_all(["Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Depraved Sanctuary Exalted Stash":                 lambda state: state.has("Strange Key", self.player),
            "Rotting Croplands Exalted Stash":                  lambda state: state.has("Rotting Croplands Destroy North Blockade",self.player),
            "Old Grove Secret Chest":                           lambda state: state.has("Old Grove Bridge Repair",self.player),
            "The Hidden Path - Dreeg":                          lambda state: state.has("Lower Crossing Destroy Blockade",self.player),
            "The Hidden Path - Solael":                         lambda state: state.has("Lower Crossing Destroy Blockade",self.player),
            "The Hidden Path - Bysmiel":                        lambda state: state.has("Lower Crossing Destroy Blockade",self.player),
            "Journal of Inquisitor Creed - 9th Entry":          lambda state: state.has("Warden Boss Door Unlock",self.player),
            "Clippings from Ivonda's Memory":                   lambda state: state.has_all(["Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Inarah, the Afflicted":                            lambda state: state.has("Tomb of Nephos Destroy Barrier",self.player),
            "Guardian of Dreeg":                                lambda state: state.has("Lower Crossing Destroy Blockade",self.player),
            "Salazar, Blade of Ch'thon":                        lambda state: state.has("Strange Key",self.player),
            "Dangerous Curiosity":                              lambda state: state.has("Devil's Crossing Revered",self.player),
            "Ellena, the First Slith":                          lambda state: state.has("Devil's Crossing Revered",self.player),
            "Guardian of Solael":                               lambda state: state.has("Lower Crossing Destroy Blockade",self.player),
            "Making a Deal":                                    lambda state: state.has_all(["Homestead Revered","Warden Boss Door Unlock","Homestead Side Doors Unlock"],self.player),
            "Death's Vigil - Kymon's Chosen Faction Quest 1":   lambda state: state.has("Homestead Side Doors Unlock",self.player),
            "Death's Vigil - Kymon's Chosen Faction Quest 2":   lambda state: state.has("Homestead Side Doors Unlock",self.player),
            "Noveria Stormfire - Master Ravok":                 lambda state: state.has("Homestead Side Doors Unlock",self.player),
            "Death's Vigil - Kymon's Chosen Faction Quest 3":   lambda state: state.has("Homestead Side Doors Unlock",self.player),
            "Death's Vigil - Kymon's Chosen Faction Quest 4":   lambda state: state.has("Homestead Side Doors Unlock",self.player),
            "Death's Vigil - Kymon's Chosen Faction Quest 5":   lambda state: state.has_all(["Death's Vigil - Kymon's Chosen Revered","Homestead Side Doors Unlock"],self.player),
            "Death's Vigil - Kymon's Chosen Faction Quest 6":   lambda state: state.has_all(["Death's Vigil - Kymon's Chosen Revered","Homestead Side Doors Unlock"],self.player),
            "Guardian of Bysmiel":                              lambda state: state.has("Lower Crossing Destroy Blockade",self.player),
            "Rhowari Legacy":                                   lambda state: state.has("Rovers Revered",self.player),
            "Herald of Destruction":                            lambda state: state.has_all(["Black Legion Revered","Homestead Side Doors Unlock"],self.player),
            "The Coven's Walls":                                lambda state: state.has_all(["Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Pruning The Weeds":                                lambda state: state.has_all(["Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Allure of the Wendigo":                            lambda state: state.has_all(["Coven of Ugdenbog Revered","Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Trapped Wraith 1":                                 lambda state: state.has_all(["Coven of Ugdenbog Revered","Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Trapped Wraith 2":                                 lambda state: state.has_all(["Coven of Ugdenbog Revered","Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Trapped Wraith 3":                                 lambda state: state.has_all(["Coven of Ugdenbog Revered","Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Power in the Circles":                             lambda state: state.has_all(["Coven of Ugdenbog Revered","Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Stone Basilisk":                                   lambda state: state.has_all(["Coven of Ugdenbog Revered","Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Final Seal":                                       lambda state: state.has_all(["Coven of Ugdenbog Revered","Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Galakros, the Mountain":                           lambda state: state.has("Malmouth Sewers Destroy Blockade",self.player),
            "Someone on the Inside":                            lambda state: state.has_all(["Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Bring out Your Dead":                              lambda state: state.has_all(["Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Secure the Blackiron Docks":                       lambda state: state.has_all(["Malmouth Resistance Revered","Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Rise of the Insurgence":                           lambda state: state.has_all(["Malmouth Resistance Revered","Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Alberran Rein":                                    lambda state: state.has_all(["Malmouth Resistance Revered","Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Dreven Cole":                                      lambda state: state.has_all(["Malmouth Resistance Revered","Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Cyrian Marcan":                                    lambda state: state.has_all(["Malmouth Resistance Revered","Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Chamber of the High Council Secret Chest":         lambda state: state.has_all(["Malmouth Resistance Revered","Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Hargate's Journal - Page 2":                       lambda state: state.has_all(["Arkovia Bridge Repair","Devil's Crossing Revered"],self.player),
            "Hargate's Journal - Page 3":                       lambda state: state.has_all(["Arkovia Bridge Repair","Devil's Crossing Revered"],self.player),
            "Hargate's Journal - Page 4":                       lambda state: state.has_all(["Arkovia Bridge Repair","Devil's Crossing Revered"],self.player),
            "Nearan's Work Log":                                lambda state: state.has_all(["Malmouth Resistance Revered","Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),
            "Council Report to Theodin Marcell":                lambda state: state.has_all(["Malmouth Resistance Revered","Homestead Main Doors Unlock","Fort Ikon Gate Unlock","Fort Ikon Destroy Blockade","Tomb of the Watchers Door Unlock","Loghorrean Seal Unlock","Homestead Side Doors Unlock"],self.player),

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
