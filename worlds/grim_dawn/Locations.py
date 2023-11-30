from typing import Callable, Dict, NamedTuple, Optional

from BaseClasses import Location, MultiWorld

baseId = 219990
nlambda = None

class GrimDawnLocation(Location):
    game = "Grim Dawn"


class GrimDawnLocationData(NamedTuple):
    region: str
    address: Optional[int] = None
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True
    locked_item: Optional[str] = None

_location_data_list: list[tuple[str,str,Optional[Callable[[MultiWorld, int], bool]]]] = [
    #normal Locations
    
    ("Rescue Faldis",                               "Act 1",                        None    ),
    ("Kill Reanimator",                             "Act 1",                        None    ),
    ("Kasparov's Device",                           "Act 1",                        None    ),
    ("Repair Waterpump",                            "Act 1",                        None    ),
    ("Cleanse Slith Infestation",                   "Act 1",                        None    ),
    ("Free the Rovers",                             "Act 1",                        None    ),
    ("Isaac's Stash",                               "Act 1",                        None    ),
    ("Rescue Luther Graves",                        "Act 1",                        None    ),
    ("Sunken Reliquary Exalted Stash",              "Flooded Passage Blockade",     None    ),
    ("Secure Wightmire Portal",                     "Act 1",                        None    ),
    ("Secure Burrwitch Portal",                     "Act 1",                        None    ),
    ("A Cultist in the Midst",                      "Act 1",                        None    ),
    ("Depraved Sanctuary Exalted Stash",            "Act 1",                        None    ),
    ("Rescue Ulgrim",                               "Act 1",                        None    ),
    ("Rescue Darlet",                               "Act 1",                        None    ),
    ("Deal with the Hermit",                        "Act 1",                        None    ),
    ("A Tale of Two Blacksmiths",                   "Act 1",                        None    ),
    ("The Seamstress",                              "Act 1",                        None    ),
    ("Monster's Hoard",                             "Act 1",                        None    ),
    ("Hallowed Hill Exalted Stash",                 "Act 1",                        None    ),
    ("Ominous Lair Exalted Stash",                  "Act 1",                        None    ),
    ("Kill Warden Krieg",                           "Warden's Cellar",              None    ),
    ("Warden Krieg Exalted Stash",                  "Warden's Cellar",              None    ),

    #Devotion Shrines

    ("Devotion Shrine - Burial Hill",               "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.devotion_shrines.value == 1),
    ("Devotion Shrine - Foggy Banks Cave",          "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.devotion_shrines.value == 1),
    ("Devotion Shrine - Burrwitch Outskirts Cave",  "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.devotion_shrines.value == 1),
    ("Devotion Shrine - Flooded Passage",           "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.devotion_shrines.value == 1),
    ("Devotion Shrine - Burrwitch",                 "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.devotion_shrines.value == 1),
    ("Devotion Shrine - Devil's Aquifer",           "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.devotion_shrines.value == 1),
    ("Devotion Shrine - Warden's Lab",              "Warden's Cellar",              lambda multiworld, player: multiworld.worlds[player].options.devotion_shrines.value == 1),
    ("Devotion Shrine - East Marsh",                "East Marsh Bridge",            lambda multiworld, player: multiworld.worlds[player].options.devotion_shrines.value == 1),

    #Lore Notes

    ("Crudely Scrawled Note",                       "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Francis's Note",                              "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Harbormaster's Log - Lower Crossing",         "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Hargate's Journal 1",                         "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Milton Hart's Note",                          "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Dirt-Covered Note",                           "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Missive to Wightmire Bloodbound",             "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("The Hidden Path - Dreeg",                     "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Writings of Rolderathis 1",                   "Flooded Passage Blockade",     lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Warden Krieg's Journal",                      "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Harbormaster's Log - Burrwitch",              "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Alister's Diary",                             "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Burrwitch Recon Report",                      "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Creed's Journal 1",                           "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Creed's Journal 2",                           "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Creed's Journal 3",                           "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Creed's Journal 4",                           "Act 1",                        lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Creed's Journal 5",                           "Warden's Cellar",              lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Creed's Journal 6",                           "Warden's Cellar",              lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Gethrand's Notes 1st Entry",                  "Warden's Cellar",              lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Gethrand's Notes 2nd Entry",                  "Warden's Cellar",              lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Gethrand's Notes Final Entry",                "Warden's Cellar",              lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Zanbrandt's Notes",                           "Warden's Cellar",              lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Missive to Warden Krieg",                     "Warden's Cellar",              lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Oboruuk's Journal 1",                         "East Marsh Bridge",            lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("The Gift of Ch'thon",                         "East Marsh Bridge",            lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),
    ("Muddy Note",                                  "East Marsh Bridge",            lambda multiworld, player: multiworld.worlds[player].options.lore.value == 1),


]


location_data_table: Dict[str, GrimDawnLocationData] = { item[0]: GrimDawnLocationData(region=item[1],can_create=(item[2] if item[2] is not None else (lambda multiworld, player: True)),address=(baseId+index)) for index,item in enumerate(_location_data_list)}


location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
locked_locations = {name: data for name, data in location_data_table.items() if data.locked_item}
