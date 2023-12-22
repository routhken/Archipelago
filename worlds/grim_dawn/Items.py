from typing import Callable, Dict, NamedTuple, Optional,TYPE_CHECKING

import random

from BaseClasses import Item, ItemClassification, MultiWorld

baseId = 219990

class GrimDawnItem(Item):
    game = "Grim Dawn"


class GrimDawnItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler
    quantity: int = 1
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True


item_data_table: Dict[str, GrimDawnItemData] = {
    #Act 1 items
    "Cultist Orders":                           GrimDawnItemData( code=baseId   , type=ItemClassification.progression, ),
    "Strange Key":                              GrimDawnItemData( code=baseId+1 , type=ItemClassification.progression, ),
    "Scrap":                                    GrimDawnItemData( code=baseId+2 , type=ItemClassification.progression, quantity=5 ),
    "Flooded Passage Destroy Blockade":         GrimDawnItemData( code=baseId+3 , type=ItemClassification.progression, can_create=lambda multiworld, player: (multiworld.worlds[player].options.one_shot.value == 1 or multiworld.worlds[player].options.lore.value == 1) ),
    "Lower Crossing Destroy Blockade":          GrimDawnItemData( code=baseId+4 , type=ItemClassification.progression, can_create=lambda multiworld, player: (multiworld.worlds[player].options.lore.value == 1) ),
    "East Marsh Bridge Repair":                 GrimDawnItemData( code=baseId+5 , type=ItemClassification.progression, can_create=lambda multiworld, player: (multiworld.worlds[player].options.lore.value == 1 or multiworld.worlds[player].options.devotion_shrine.value == 1) ),
    "Warden's Cellar Unlock":                   GrimDawnItemData( code=baseId+6 , type=ItemClassification.progression, ),
    #Act 2 and 3 items
    "Arkovia Bridge Repair":                    GrimDawnItemData( code=baseId+7 , type=ItemClassification.progression, can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1) ),
    "Arkovian Foothills Destroy Barricade":     GrimDawnItemData( code=baseId+8 , type=ItemClassification.progression, can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1) ),
    "New Harbor Destroy Barricade":             GrimDawnItemData( code=baseId+9 , type=ItemClassification.progression, can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1 and multiworld.worlds[player].options.secret_chest.value == 1) ),
    "Prospector's Trail Destroy Barricade":     GrimDawnItemData( code=baseId+10, type=ItemClassification.progression, can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1) ),
    "Twin Falls Bridge Repair":                 GrimDawnItemData( code=baseId+11, type=ItemClassification.progression, can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1) ),
    "Homestead Side Doors Unlock":              GrimDawnItemData( code=baseId+12, type=ItemClassification.progression, can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1) ),
    "Rotting Croplands Destroy South Blockade": GrimDawnItemData( code=baseId+13, type=ItemClassification.progression, can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1) ),
    "Rotting Croplands Destroy North Blockade": GrimDawnItemData( code=baseId+14, type=ItemClassification.progression, can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1 and multiworld.worlds[player].options.one_shot.value == 1) ),
    "Royal Hive Queen Door Unlock":             GrimDawnItemData( code=baseId+15, type=ItemClassification.progression, can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1) ),
    "Conflagration Destroy Barricade":          GrimDawnItemData( code=baseId+16, type=ItemClassification.progression, can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1 and multiworld.worlds[player].options.forbidden_dungeons.value == 1) ),
    #Act 4 items
    "Homestead Main Doors Unlock":              GrimDawnItemData( code=baseId+17, type=ItemClassification.progression, can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2) ),
    "Darkvale Gate Boss Door Unlock":           GrimDawnItemData( code=baseId+18, type=ItemClassification.progression, can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2) ),


    "Wightmire Bridge Repair":                  GrimDawnItemData( code=baseId+19, type=ItemClassification.useful ),
    "Skill Points":                             GrimDawnItemData( code=baseId+20, type=ItemClassification.useful, can_create=lambda multiworld, player: False ),

    "Aether Crystals":                          GrimDawnItemData( code=baseId+21, type=ItemClassification.filler, can_create=lambda multiworld, player: False ),
    "Extra EXP":                                GrimDawnItemData( code=baseId+22, type=ItemClassification.filler, can_create=lambda multiworld, player: False ),

    "Calamity":                                 GrimDawnItemData( code=baseId+23, type=ItemClassification.useful, can_create=lambda multiworld, player: False),
    "Ruination":                                GrimDawnItemData( code=baseId+24, type=ItemClassification.useful, can_create=lambda multiworld, player: False),
    "Equilibrium":                              GrimDawnItemData( code=baseId+25, type=ItemClassification.useful, can_create=lambda multiworld, player: False),
    "Glacier":                                  GrimDawnItemData( code=baseId+26, type=ItemClassification.useful, can_create=lambda multiworld, player: False),
    "Squall":                                   GrimDawnItemData( code=baseId+27, type=ItemClassification.useful, can_create=lambda multiworld, player: False),
    "Inferno":                                  GrimDawnItemData( code=baseId+28, type=ItemClassification.useful, can_create=lambda multiworld, player: False),
    "Corruption":                               GrimDawnItemData( code=baseId+29, type=ItemClassification.useful, can_create=lambda multiworld, player: False),
    "Sanctuary":                                GrimDawnItemData( code=baseId+30, type=ItemClassification.useful, can_create=lambda multiworld, player: False),
    "Guile":                                    GrimDawnItemData( code=baseId+31, type=ItemClassification.useful, can_create=lambda multiworld, player: False),
    "Rampage":                                  GrimDawnItemData( code=baseId+32, type=ItemClassification.useful, can_create=lambda multiworld, player: False),
    "Mistborne Talisman":                       GrimDawnItemData( code=baseId+33, type=ItemClassification.useful, can_create=lambda multiworld, player: False),
    "Bladesworn Talisman":                      GrimDawnItemData( code=baseId+34, type=ItemClassification.useful, can_create=lambda multiworld, player: False),
    "Gunslinger Talisman":                      GrimDawnItemData( code=baseId+35, type=ItemClassification.useful, can_create=lambda multiworld, player: False),

    "Skeleton Key":                             GrimDawnItemData( code=baseId+36, type=ItemClassification.progression, can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1 and multiworld.worlds[player].options.forbidden_dungeons.value == 1)),

}

relic_table = [
    "Calamity",
	"Ruination",
	"Equilibrium",
	"Glacier",
	"Squall",
	"Inferno",
	"Corruption",
	"Sanctuary",
	"Guile",
	"Rampage",
	"Mistborne Talisman",
	"Bladesworn Talisman",
	"Gunslinger Talisman",
]

def get_unique_relic(rand: random.Random) -> str:
    if len(get_unique_relic.local_relic_table) > 0:
        rand.shuffle( get_unique_relic.local_relic_table)
        return get_unique_relic.local_relic_table.pop()
    else:
        return ""
    
get_unique_relic.local_relic_table = relic_table.copy()

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
