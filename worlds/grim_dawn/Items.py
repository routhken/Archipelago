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
        quantity=2
    ),
    "Scrap": GrimDawnItemData(
        code=baseId+3,
        type=ItemClassification.progression,
        quantity=11
    ),
    "Iron Bits": GrimDawnItemData(
        code=baseId+4,
        type=ItemClassification.filler,
    ),
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
