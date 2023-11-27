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
    "Cultist Orders": GrimDawnItemData(
        code=baseId,
        type=ItemClassification.progression,
    ),
    "Strange Key": GrimDawnItemData(
        code=baseId+1,
        type=ItemClassification.progression,
    ),
    "Dynamite": GrimDawnItemData(
        code=baseId+2,
        type=ItemClassification.progression,
        quantity=3
    ),
    "Scrap": GrimDawnItemData(
        code=baseId+3,
        type=ItemClassification.progression,
        quantity=6
    ),
    "Burial Cave Door": GrimDawnItemData(
        code=baseId+4,
        type=ItemClassification.progression,
    ),
    "Rover Cavern Door": GrimDawnItemData(
        code=baseId+5,
        type=ItemClassification.progression,
    ),
    "Flooded Passage Door": GrimDawnItemData(
        code=baseId+6,
        type=ItemClassification.progression,
    ),
    "River Passage Door": GrimDawnItemData(
        code=baseId+7,
        type=ItemClassification.progression,
    ),
    "Festering Lair Door": GrimDawnItemData(
        code=baseId+8,
        type=ItemClassification.progression,
    ),
    "Dank Cellar Door": GrimDawnItemData(
        code=baseId+9,
        type=ItemClassification.progression,
    ),
    "Warden's Cellar Door": GrimDawnItemData(
        code=baseId+10,
        type=ItemClassification.progression,
    ),
    "Iron Bits": GrimDawnItemData(
        code=baseId+11,
        type=ItemClassification.filler,
        can_create=lambda multiworld, player: False
    ), #only create as overflow, we don't need any
    "Draining the Flooded Passage": GrimDawnItemData(
        code=None,
        type=ItemClassification.progression,
        quantity=1
    )
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
