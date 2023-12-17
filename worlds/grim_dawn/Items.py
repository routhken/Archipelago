from typing import Callable, Dict, NamedTuple, Optional

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
    "Cultist Orders": GrimDawnItemData( code=baseId, type=ItemClassification.progression, ),
    "Strange Key": GrimDawnItemData( code=baseId+1, type=ItemClassification.progression, ),
    "Dynamite": GrimDawnItemData( code=baseId+2, type=ItemClassification.useful, quantity=2 ),
    "Scrap": GrimDawnItemData( code=baseId+3, type=ItemClassification.progression, quantity=5 ),
    "Flooded Passage Destroy Blockade": GrimDawnItemData( code=baseId+4, type=ItemClassification.progression, ),
    "Lower Crossing Destroy Blockade": GrimDawnItemData( code=baseId+5, type=ItemClassification.progression, ),
    "East Marsh Bridge Repair": GrimDawnItemData( code=baseId+6, type=ItemClassification.progression, ),
    "Arkovia Bridge Repair": GrimDawnItemData( code=baseId+7, type=ItemClassification.progression, ),
    "Warden's Cellar Door": GrimDawnItemData( code=baseId+8, type=ItemClassification.progression, ),
    "Wightmire Bridge Repair": GrimDawnItemData( code=baseId+9, type=ItemClassification.useful ),
    "Level Up": GrimDawnItemData( code=baseId+10, type=ItemClassification.useful, quantity=2 ),
    "Skill Points": GrimDawnItemData( code=baseId+11, type=ItemClassification.useful, quantity=2 ),
    "Aether Crystals": GrimDawnItemData( code=baseId+12, type=ItemClassification.filler, quantity=2 ),
    "Extra EXP": GrimDawnItemData( code=baseId+13, type=ItemClassification.filler, quantity=2 ),

}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
