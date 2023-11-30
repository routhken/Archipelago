from typing import Dict, List, NamedTuple


class GrimDawnRegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, GrimDawnRegionData] = {
    "Menu": GrimDawnRegionData(["Act 1"]),
    "Act 1": GrimDawnRegionData(["Flooded Passage Blockade","Warden's Cellar","East Marsh Bridge"]),
    "Flooded Passage Blockade": GrimDawnRegionData(),
    "Warden's Cellar": GrimDawnRegionData(),
    "East Marsh Bridge": GrimDawnRegionData(),
}
