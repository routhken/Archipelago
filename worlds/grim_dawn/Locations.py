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
        region="Act 1",
        address=baseId,
    ),
    "Kasparov's Device": GrimDawnLocationData(
        region="Act 1",
        address=baseId+1,
    ),
    "Repair Waterpump": GrimDawnLocationData(
        region="Act 1",
        address=baseId+2,
    ),
    "Cleanse Slith Infestation": GrimDawnLocationData(
        region="Act 1",
        address=baseId+3,
    ),
    "Free the Rovers": GrimDawnLocationData(
        region="Act 1",
        address=baseId+4,
    ),
    "Rescue Survivor": GrimDawnLocationData(
        region="Act 1",
        address=baseId+5,
    ),
    "Avenge Isaac": GrimDawnLocationData(
        region="Act 1",
        address=baseId+6,
    ),
    "Retrieve Isaac's Stash": GrimDawnLocationData(
        region="Act 1",
        address=baseId+7,
    ),
    "Rescue Luther Graves": GrimDawnLocationData(
        region="Act 1",
        address=baseId+8,
    ),
    "Repair Wightmire Bridge": GrimDawnLocationData(
        region="Act 1",
        address=baseId+9,
    ),
    "Secure Burrwitch Portal": GrimDawnLocationData(
        region="Act 1",
        address=baseId+10,
    ),
    "Confront Direni": GrimDawnLocationData(
        region="Act 1",
        address=baseId+11,
    ),
    "Rescue Ulgrim": GrimDawnLocationData(
        region="Act 1",
        address=baseId+12,
    ),
    "Destroy Debris Blocking East Marsh": GrimDawnLocationData(
        region="Act 1",
        address=baseId+13,
    ),
    "Repair Bridge to East Marsh": GrimDawnLocationData(
        region="Act 1",
        address=baseId+14,
    ),
    "Rescue Darlet": GrimDawnLocationData(
        region="Act 1",
        address=baseId+15,
    ),
    "Deal with the Hermit": GrimDawnLocationData(
        region="Act 1",
        address=baseId+16,
    ),
    "Obtain Hart's Amulet": GrimDawnLocationData(
        region="Act 1",
        address=baseId+17,
    ),
    "Harmond's Request": GrimDawnLocationData(
        region="Act 1",
        address=baseId+18,
    ),
    "Deliver Menhir": GrimDawnLocationData(
        region="Act 1",
        address=baseId+19,
    ),
    "Kill Warden Krieg": GrimDawnLocationData(
        region="Act 1",
        address=baseId+20,
    ),
    "Open Krieg's Exalted Stash": GrimDawnLocationData(
        region="Act 1",
        address=baseId+21,
    ),
    "Depraved Sanctuary Chest": GrimDawnLocationData(
        region="Act 1",
        address=baseId+22,
    ),
    "Bring Fabric to Constance": GrimDawnLocationData(
        region="Act 1",
        address=baseId+23,
    ),
}

location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
locked_locations = {name: data for name, data in location_data_table.items() if data.locked_item}
