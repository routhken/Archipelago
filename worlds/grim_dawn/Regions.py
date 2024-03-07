from typing import Dict, List, NamedTuple, Callable

from BaseClasses import MultiWorld

class GrimDawnRegionData(NamedTuple):
    connecting_regions: List[str] = []
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True


region_data_table: Dict[str, GrimDawnRegionData] = {
    "Menu":                 GrimDawnRegionData(connecting_regions=["Act 1"]),
    "Act 1":                GrimDawnRegionData(connecting_regions=["Sunken Reliquary","East Marsh","Act 2","Devil's Aquifer","Warden's Cellar"]),
    "Devil's Aquifer":      GrimDawnRegionData(connecting_regions=[]),
    "Sunken Reliquary":     GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.one_shot.value == 1 or multiworld.worlds[player].options.lore.value == 1)),
    "East Marsh":           GrimDawnRegionData(connecting_regions=["Temple of the Three"]),
    "Warden's Cellar":      GrimDawnRegionData(connecting_regions=[]),
    "Act 2":                GrimDawnRegionData(connecting_regions=["Act 3"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1)),
    "Act 3":                GrimDawnRegionData(connecting_regions=["Steps of Torment","Port Valbury","Four Hills Secret","Tyrant's Hold","Homestead Side Doors","Act 4"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1)),
    "Steps of Torment":     GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1)),
    "Four Hills Secret":    GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1)),
    "Tyrant's Hold":        GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1)),
    "Port Valbury":         GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1)),
    "Homestead Side Doors": GrimDawnRegionData(connecting_regions=["Royal Hive"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1)),
    "Royal Hive":           GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 1)),
    "Act 4":                GrimDawnRegionData(connecting_regions=["Act 5"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2)),
    "Temple of the Three":  GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2)),
    "Act 5":                GrimDawnRegionData(connecting_regions=["Act 6","Act 7"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2)),
    "Act 6":                GrimDawnRegionData(connecting_regions=["Tomb of the Watchers","Bastion of Chaos"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2)),
    "Bastion of Chaos":     GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2)),
    "Tomb of the Watchers": GrimDawnRegionData(connecting_regions=["Edge of Madness"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2)),
    "Edge of Madness":      GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2)),
    "Act 7":                GrimDawnRegionData(connecting_regions=["Nane's Hideout","Ancient Grove","Forlorn Cellar","Den of the Ancient","Act 8"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    "Nane's Hideout":       GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    "Ancient Grove":        GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    "Den of the Ancient":   GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    "Forlorn Cellar":       GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    "Act 8":                GrimDawnRegionData(connecting_regions=["Candle District","Act 9"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    "Candle District":      GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    "Act 9":                GrimDawnRegionData(connecting_regions=["Candle District","Harbor Stash","Crown Hill"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    "Harbor Stash":         GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    "Crown Hill":           GrimDawnRegionData(connecting_regions=["Fleshworks"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    "Fleshworks":           GrimDawnRegionData(connecting_regions=["Sanctum of Flesh"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    "Sanctum of Flesh":     GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
}
