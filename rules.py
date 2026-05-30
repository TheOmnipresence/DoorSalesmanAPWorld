from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from .world import DoorSalesmanWorld


repairs_to = {
    "Knobless Base Door": "Base Door",
    "Scratched Door": "Plain Door",
    "Cracked Oak Door": "Oak Door",
    "Hole Oak Door": "Oak Door",
    "Ripped Screen Door": "Screen Door",
    "Fractured Ewhs Door": "Ewhs Door",
    "Rough Blue Door": "Blue Door",
    "Fractured Glass Door": "Glass Door",
    "Cracked Mansion Door": "Mansion Door",
    "Wheelless Steel Door": "Steel Door",
    "Melted Door": "Ice Door",
}
repair_requirements = {
    "Fractured Ewhs Door": ["Glassworking"],
    "Fractured Glass Door": ["Glassworking"],
    "Melted Door": ["Freezer"],
}
## what these doors sell for
door_prices = {
    "Base Door": 45,
    "Knobless Base Door": 35,
    "Plain Door": 55,
    "Scratched Door": 30,
    "Oak Door": 100,
    "Cracked Oak Door": 75,
    "Hole Oak Door": 40,
    "Ripped Screen Door": 5,
    "Screen Door": 55,
    "Ewhs Door": 115,
    "Fractured Ewhs Door": 90,
    "Blue Door": 90,
    "Rough Blue Door": 70,
    "Gold Oak Door": 250,
    "Glass Door": 130,
    "Fractured Glass Door": 40,
    "Mansion Door": 110,
    "Cracked Mansion Door": 85,
    "Steel Door": 750,
    "Wheelless Steel Door": 600,
    "Ice Door": 235,
    "Melted Door": 135,
}
shop_costs = {
    "Warehouse shop item 1": 45,
    "Warehouse shop item 2": 20,
    "Warehouse shop item 3": 20,
    "Shrimpville shop item 1": 15,
    "Shrimpville shop item 2": 90,
    "Shrimpville shop item 3": 210,
    "Fancytown shop item 1": 60,
    "Fancytown shop item 2": 190,
    "Mansion Lane shop item 1": 45,
    "Mansion Lane shop item 2": 110,
    "Mansion Lane shop item 3": 30,
    #coldington
    "Industrial Zone shop item 1": 50,
    "Industrial Zone shop item 2": 190,
    "Industrial Zone shop item 3": 540,
}
npc_wants = {
    "May": ["Base Door", "Oak Door"],
    "Doug": ["Base Door", "Oak Door", "Screen Door"],
    "Mr Brown": ["Base Door", "Oak Door", "Scratched Door", "Screen Door", "Plain Door"],
    "Liliana": ["Ewhs Door", "Blue Door"],
    "Ice Man": ["Ice Door"],

    "Poshman": ["Oak Door"],
    "Hole Guy": ["Oak Door"],
    "Gold": ["Gold Oak Door"],

    "John Bottom": ["Blue Door", "Mansion Door"],
    "John Top": ["Glass Door"],

    "Dr Lebut": ["Ice Door"],
}
neighborhood_populations = {
    "Workshop": [],
    "Shrimpville": ["May", "Doug", "Mr Brown", "Liliana", "Ice Man"],
    "Fancytown": ["Poshman", "Hole Guy", "Gold"],
    "Mansion Lane": ["John Bottom", "John Top"],
    "Coldington": ["Dr Lebut"],
    "Industrial Zone": [],
}
def get_area_sells() -> dict:
    result = {}
    for i in neighborhood_populations:
        result[i] = []
        for npc in neighborhood_populations[i]:
            for door in npc_wants[npc]:
                if not result[i].__contains__(door):
                    result[i].append(door)
    return result
area_sells = get_area_sells()
unlock_npcs = {
    "Mansion Lane": "Gold",
    "Coldington": "Ice Man",
}


def has_door(door: str, state: CollectionState, world: DoorSalesmanWorld) -> bool:
    if state.has(door, world.player):
        return True

    for i in repairs_to:
        if repairs_to[i] == door:
            if repair_requirements.__contains__(i):
                if state.has_all([i] + repair_requirements[i], world.player):
                    return True
            else:
                if state.has(i, world.player):
                    return True
    return False


def can_repair_door(door: str, state: CollectionState, world: DoorSalesmanWorld) -> bool:
    if not repair_requirements.__contains__(door):
        return True
    return state.has_any(repair_requirements[door], world.player)


def can_repair_all_variants(door: str, state: CollectionState, world: DoorSalesmanWorld) -> bool:
    for i in repairs_to:
        if repairs_to[i] == door:
            if not can_repair_door(door, state, world):
                return False
    return True


def can_meet_cost(cost: int, state: CollectionState, world: DoorSalesmanWorld) -> bool:
    money = 0
    for area in area_sells:
        if not can_access_area(area, state, world):
            continue
        for door in area_sells[area]:
            if has_door(door, state, world):
                if can_repair_all_variants(door, state, world):
                    return True
                else:
                    money += door_prices[door] * state.prog_items[world.player][door]
                    if money >= cost:
                        return True

    return False


def can_access_area(area: str, state: CollectionState, world: DoorSalesmanWorld) -> bool:
    if ["Workshop", "Shrimpville", "Fancytown"].__contains__(area):
        return True
    elif area == "Industrial Zone":
        return state.has_all(["Toolkit", "Glassworking"], world.player)
    else:
        return state.has(area + " neighborhood unlock", world.player)


def can_get_shop_item(item: str, state: CollectionState, world: DoorSalesmanWorld) -> bool:
    if not can_access_area(item.split(" shop item ")[0], state, world):
        return False
    if shop_costs[item] >= 90:
        return True
    return can_meet_cost(shop_costs[item], state, world)


def can_complete_npc(npc: str, state: CollectionState, world: DoorSalesmanWorld) -> bool:
    lives = ""
    for i in neighborhood_populations:
        if neighborhood_populations[i].__contains__(npc):
            lives = i
            break
    if not can_access_area(lives, state, world):
        return False
    for i in npc_wants:
        if has_door(i, state, world):
            return True
    return False


def set_all_rules(world: DoorSalesmanWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: DoorSalesmanWorld) -> None:
   pass


def set_all_location_rules(world: DoorSalesmanWorld) -> None:

    for i in shop_costs:
        set_rule(world.get_location(i), lambda state: can_get_shop_item(i, state, world))
    for i in npc_wants:
        set_rule(world.get_location(i + " Old Door"), lambda state: can_complete_npc(i, state, world))
    for i in unlock_npcs:
        set_rule(world.get_location(i + " neighborhood unlock"), lambda state: can_complete_npc(unlock_npcs[i], state, world))


def set_completion_condition(world: DoorSalesmanWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Coldington neighborhood unlock", world.player)
