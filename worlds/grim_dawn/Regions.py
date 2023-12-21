from typing import Dict, List, NamedTuple


class GrimDawnRegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, GrimDawnRegionData] = {
    "Menu": GrimDawnRegionData(["Act 1"]),
    "Act 1": GrimDawnRegionData(["Warden's Cellar","Flooded Passage","East Marsh","Act 2"]),
    "Warden's Cellar": GrimDawnRegionData(),
    "Flooded Passage": GrimDawnRegionData(),
    "East Marsh": GrimDawnRegionData(),
    "Act 2": GrimDawnRegionData(["Act 3"]),
    "Act 3": GrimDawnRegionData(["New Harbor","Desert","Homestead Side Doors","Conflagration","Act 4"]),
    "New Harbor": GrimDawnRegionData(),
    "Desert": GrimDawnRegionData(),
    "Conflagration": GrimDawnRegionData(),
    "Homestead Side Doors": GrimDawnRegionData(),
    "Act 4": GrimDawnRegionData(["Darkvale Gate"]),
    "Darkvale Gate": GrimDawnRegionData(),
}
