from typing import Dict, List, NamedTuple


class GrimDawnRegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, GrimDawnRegionData] = {
    "Menu":                 GrimDawnRegionData(connecting_regions=["Act 1"]),
    "Act 1":                GrimDawnRegionData(connecting_regions=["Sunken Reliquary","East Marsh","Act 2","Devil's Aquifer","Warden's Cellar"]),
    "Devil's Aquifer":      GrimDawnRegionData(connecting_regions=[]),
    "Sunken Reliquary":     GrimDawnRegionData(connecting_regions=[]),
    "East Marsh":           GrimDawnRegionData(connecting_regions=["Temple of the Three"]),
    "Warden's Cellar":      GrimDawnRegionData(connecting_regions=[]),
    "Act 2":                GrimDawnRegionData(connecting_regions=["Act 3"]),
    "Act 3":                GrimDawnRegionData(connecting_regions=["Steps of Torment","Port Valbury","Four Hills Secret","Tyrant's Hold","Homestead Side Doors","Act 4"]),
    "Steps of Torment":     GrimDawnRegionData(connecting_regions=[]),
    "Four Hills Secret":    GrimDawnRegionData(connecting_regions=[]),
    "Tyrant's Hold":        GrimDawnRegionData(connecting_regions=[]),
    "Port Valbury":         GrimDawnRegionData(connecting_regions=[]),
    "Homestead Side Doors": GrimDawnRegionData(connecting_regions=["Royal Hive"]),
    "Royal Hive":           GrimDawnRegionData(connecting_regions=[]),
    "Act 4":                GrimDawnRegionData(connecting_regions=["Act 5"]),
    "Temple of the Three":  GrimDawnRegionData(connecting_regions=[]),
    "Act 5":                GrimDawnRegionData(connecting_regions=["Act 6","Act 7"]),
    "Act 6":                GrimDawnRegionData(connecting_regions=["Tomb of the Watchers","Bastion of Chaos"]),
    "Bastion of Chaos":     GrimDawnRegionData(connecting_regions=[]),
    "Tomb of the Watchers": GrimDawnRegionData(connecting_regions=["Edge of Madness"]),
    "Edge of Madness":      GrimDawnRegionData(connecting_regions=[]),
    "Act 7":                GrimDawnRegionData(connecting_regions=["Nane's Hideout","Ancient Grove","Forlorn Cellar","Den of the Ancient","Act 8"]),
    "Nane's Hideout":       GrimDawnRegionData(connecting_regions=[]),
    "Ancient Grove":        GrimDawnRegionData(connecting_regions=[]),
    "Den of the Ancient":   GrimDawnRegionData(connecting_regions=[]),
    "Forlorn Cellar":       GrimDawnRegionData(connecting_regions=[]),
    "Act 8":                GrimDawnRegionData(connecting_regions=["Candle District","Act 9"]),
    "Candle District":      GrimDawnRegionData(connecting_regions=[]),
    "Act 9":                GrimDawnRegionData(connecting_regions=["Candle District","Harbor Stash","Crown Hill"]),
    "Harbor Stash":         GrimDawnRegionData(connecting_regions=[]),
    "Crown Hill":           GrimDawnRegionData(connecting_regions=["Fleshworks"]),
    "Fleshworks":           GrimDawnRegionData(connecting_regions=["Sanctum of Flesh"]),
    "Sanctum of Flesh":     GrimDawnRegionData(connecting_regions=[]),
}
