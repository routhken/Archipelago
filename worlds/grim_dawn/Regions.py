from typing import Dict, List, NamedTuple


class GrimDawnRegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, GrimDawnRegionData] = {
    "Menu": GrimDawnRegionData(["Act 1"]),
    "Act 1": GrimDawnRegionData(["Burial Cave","Rover Cavern","Post Flooded Passage"]),
    "Burial Cave": GrimDawnRegionData(["Post Water Pump"]),
    "Post Water Pump": GrimDawnRegionData(),
    "Rover Cavern": GrimDawnRegionData(),
    "Post Flooded Passage": GrimDawnRegionData(["Warden's Cellar","Dank Cellar","Festering Lair","River Passage"]),
    "Dank Cellar": GrimDawnRegionData(),
    "Festering Lair": GrimDawnRegionData(),
    "River Passage": GrimDawnRegionData(),
    "Warden's Cellar": GrimDawnRegionData()
}
