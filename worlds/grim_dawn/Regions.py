from typing import Dict, List, NamedTuple


class GrimDawnRegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, GrimDawnRegionData] = {
    "Menu": GrimDawnRegionData(["Act 1"]),
    "Act 1": GrimDawnRegionData(),
}
