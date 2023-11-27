from typing import Callable, Dict, NamedTuple, Optional

from BaseClasses import Location, MultiWorld

baseId = 219990

class GrimDawnLocation(Location):
    game = "Grim Dawn"


class GrimDawnLocationData(NamedTuple):
    region: str
    address: Optional[int] = None
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True
    locked_item: Optional[str] = None


location_data_table: Dict[str, GrimDawnLocationData] = {
    "Kill Reanimator": GrimDawnLocationData(
        region="Burial Cave",
        address=baseId,
    ),
    "Kasparov's Device": GrimDawnLocationData(
        region="Burial Cave",
        address=baseId+1,
    ),
    "Repair Waterpump": GrimDawnLocationData(
        region="Burial Cave",
        address=baseId+2,
    ),
    "Cleanse Slith Infestation": GrimDawnLocationData(
        region="Post Water Pump",
        address=baseId+3,
    ),
    "Free the Rovers": GrimDawnLocationData(
        region="Rover Cavern",
        address=baseId+4,
    ),
    "Rescue Faldis": GrimDawnLocationData(
        region="Act 1",
        address=baseId+5,
    ),
    "Isaac's Stash": GrimDawnLocationData(
        region="Act 1",
        address=baseId+6,
    ),
    "Rescue Luther Graves": GrimDawnLocationData(
        region="Act 1",
        address=baseId+7,
    ),
    "Sunken Reliquary Exalted Stash": GrimDawnLocationData(
        region="Post Flooded Passage",
        address=baseId+8,
    ),
    "A Cultist in the Midst": GrimDawnLocationData(
        region="Post Flooded Passage",
        address=baseId+9,
    ),
    "Depraved Sanctuary Exalted Stash": GrimDawnLocationData(
        region="Post Flooded Passage",
        address=baseId+10,
    ),
    "Rescue Ulgrim": GrimDawnLocationData(
        region="Post Flooded Passage",
        address=baseId+11,
    ),
    "Rescue Darlet": GrimDawnLocationData(
        region="Dank Cellar",
        address=baseId+12,
    ),
    "Deal with the Hermit": GrimDawnLocationData(
        region="Post Flooded Passage",
        address=baseId+13,
    ),
    "A Tale of Two Blacksmiths": GrimDawnLocationData(
        region="Post Flooded Passage",
        address=baseId+14,
    ),
    "The Seamstress": GrimDawnLocationData(
        region="Post Flooded Passage",
        address=baseId+15,
    ),
    "Monster's Hoard": GrimDawnLocationData(
        region="Festering Lair",
        address=baseId+16,
    ),
    "Secure Burrwitch Portal": GrimDawnLocationData(
        region="Post Flooded Passage",
        address=baseId+17,
    ),
    "Hallowed Hill Exalted Stash": GrimDawnLocationData(
        region="River Passage",
        address=baseId+18,
    ),
    "Ominous Lair Exalted Stash": GrimDawnLocationData(
        region="Warden's Cellar",
        address=baseId+19,
    ),
    "Kill Warden Krieg": GrimDawnLocationData(
        region="Warden's Cellar",
        address=baseId+20,
    ),
    "Warden Krieg Exalted Stash": GrimDawnLocationData(
        region="Warden's Cellar",
        address=baseId+21,
    ),
    "Draining the Flooded Passage": GrimDawnLocationData(
        region="Act 1",
        address=None,
        locked_item="Draining the Flooded Passage"
    )
}

location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
locked_locations = {name: data for name, data in location_data_table.items() if data.locked_item}
