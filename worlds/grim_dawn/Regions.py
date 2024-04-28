from typing import Dict, List, NamedTuple, Callable

from BaseClasses import MultiWorld

class GrimDawnRegionData(NamedTuple):
    connecting_regions: List[str] = []
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True


region_data_table: Dict[str, GrimDawnRegionData] = {
    "Menu":                     GrimDawnRegionData(connecting_regions=["Act 1"]),
    "Act 1":                    GrimDawnRegionData(connecting_regions=["Sunken Reliquary","East Marsh","Act 2","Devil's Aquifer","Warden's Cellar"]),
    "Devil's Aquifer":          GrimDawnRegionData(connecting_regions=[]),
    "Sunken Reliquary":         GrimDawnRegionData(connecting_regions=[]),
    "East Marsh":               GrimDawnRegionData(connecting_regions=["Temple of the Three"]),
    "Warden's Cellar":          GrimDawnRegionData(connecting_regions=["Act 10"]),
    "Act 2":                    GrimDawnRegionData(connecting_regions=["Act 3"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2)),
    "Act 3":                    GrimDawnRegionData(connecting_regions=["Steps of Torment","Port Valbury","Four Hills Secret","Tyrant's Hold","Homestead Side Doors","Act 4"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2)),
    "Steps of Torment":         GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2) and (multiworld.worlds[player].options.forbidden_dungeons)),
    "Four Hills Secret":        GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2) and (multiworld.worlds[player].options.secret_chest)),
    "Tyrant's Hold":            GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2)),
    "Port Valbury":             GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2) and (multiworld.worlds[player].options.forbidden_dungeons)),
    "Homestead Side Doors":     GrimDawnRegionData(connecting_regions=["Royal Hive"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2)),
    "Royal Hive":               GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 2)),
    "Act 4":                    GrimDawnRegionData(connecting_regions=["Act 5"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    "Temple of the Three":      GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    "Act 5":                    GrimDawnRegionData(connecting_regions=["Act 6","Act 7"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    "Act 6":                    GrimDawnRegionData(connecting_regions=["Tomb of the Watchers","Bastion of Chaos"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    "Bastion of Chaos":         GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3) and (multiworld.worlds[player].options.forbidden_dungeons)),
    "Tomb of the Watchers":     GrimDawnRegionData(connecting_regions=["Edge of Madness"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    "Edge of Madness":          GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 3)),
    "Act 7":                    GrimDawnRegionData(connecting_regions=["Nane's Hideout","Ancient Grove","Forlorn Cellar","Den of the Ancient","Act 8"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 4)),
    "Nane's Hideout":           GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 4) and (multiworld.worlds[player].options.one_shot)),
    "Ancient Grove":            GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 4) and (multiworld.worlds[player].options.forbidden_dungeons)),
    "Den of the Ancient":       GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 4)),
    "Forlorn Cellar":           GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 4)),
    "Act 8":                    GrimDawnRegionData(connecting_regions=["Candle District","Act 9"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 4)),
    "Candle District":          GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 4)),
    "Act 9":                    GrimDawnRegionData(connecting_regions=["Candle District","Harbor Stash","Crown Hill"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 4)),
    "Harbor Stash":             GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 4) and (multiworld.worlds[player].options.one_shot)),
    "Crown Hill":               GrimDawnRegionData(connecting_regions=["Fleshworks"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 4)),
    "Fleshworks":               GrimDawnRegionData(connecting_regions=["Sanctum of Flesh"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 4)),
    "Sanctum of Flesh":         GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.goal.value >= 4)),
    "Act 10":                   GrimDawnRegionData(connecting_regions=["Act 11"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.dlc_fg)),
    "Act 11":                   GrimDawnRegionData(connecting_regions=["Lost Oasis","Tomb of the Eldritch Sun"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.dlc_fg.value)),
    "Lost Oasis":               GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.dlc_fg) and (multiworld.worlds[player].options.forbidden_dungeons)),
    "Tomb of the Eldritch Sun": GrimDawnRegionData(connecting_regions=["The Eldritch Gate"],can_create=lambda multiworld, player: (multiworld.worlds[player].options.dlc_fg)),
    "The Eldritch Gate":        GrimDawnRegionData(connecting_regions=[],can_create=lambda multiworld, player: (multiworld.worlds[player].options.dlc_fg)),

}
