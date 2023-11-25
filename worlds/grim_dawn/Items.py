from typing import Callable, Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification, MultiWorld

baseId = 219990

class GrimDawnItem(Item):
    game = "Grim Dawn"


class GrimDawnItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True


item_data_table: Dict[str, GrimDawnItemData] = {
    "Isaac's Knowledge": GrimDawnItemData(
        code=baseId,
        type=ItemClassification.progression,
    ),
    "Cultist Orders": GrimDawnItemData(
        code=baseId+1,
        type=ItemClassification.progression,
    ),
    "Menhir": GrimDawnItemData(
        code=baseId+2,
        type=ItemClassification.progression,
    ),
    "Strange Key": GrimDawnItemData(
        code=baseId+3,
        type=ItemClassification.progression,
    ),
    "Scrap": GrimDawnItemData(
        code=baseId+4,
        type=ItemClassification.filler,
        can_create=lambda multiworld, player: False
    ),
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
