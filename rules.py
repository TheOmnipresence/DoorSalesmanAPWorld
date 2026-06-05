from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule

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
repair_costs = {
    "Knobless Base Door": 5,
    "Scratched Door": 5,
    "Cracked Oak Door": 10,
    "Hole Oak Door": 20,
    "Ripped Screen Door": 10,
    "Fractured Ewhs Door": 15,
    "Rough Blue Door": 10,
    "Fractured Glass Door": 40,
    "Cracked Mansion Door": 15,
    "Wheelless Steel Door": 30,
    "Melted Door": 5,
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
    "Brick Door": 165,
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
    "Coldington shop item 1": 800,
    "Industrial Zone shop item 1": 50,
    "Industrial Zone shop item 2": 190,
    "Industrial Zone shop item 3": 540,
    "Industrial Zone shop item 4": 140,
    "Industrial Zone shop item 5": 400,
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
    "Soccer Player": ["Brick Door"],

    "Jeff": ["Steel Door"],
}
neighborhood_populations = {
    "Warehouse": [],
    "Shrimpville": ["May", "Doug", "Mr Brown", "Liliana", "Ice Man"],
    "Fancytown": ["Poshman", "Hole Guy", "Gold"],
    "Mansion Lane": ["John Bottom", "John Top"],
    "Coldington": ["Dr Lebut", "Soccer Player"],
    "Industrial Zone": ["Jeff"],
    "Junk Pit": [],
}
def get_area_sells() -> dict:
    result = {}
    for i in neighborhood_populations:
        result[i] = []
        for npc in neighborhood_populations[i]:
            for door in npc_wants[npc]:
                if not door in result[i]:
                    result[i].append(door)
    return result
area_sells = get_area_sells()
unlock_npcs = {
    "Mansion Lane": "Gold",
    "Coldington": "Ice Man",
    "Junk Pit": "Soccer Player",
}
NEIGHBORHOOD_CONNECTIONS = {
    "Warehouse": ["Shrimpville", "Fancytown", "Industrial Zone"],
    "Shrimpville": ["Coldington"],
    "Fancytown": ["Mansion Lane"],
    "Mansion Lane": [],
    "Coldington": [],
    "Industrial Zone": ["Junk Pit"],
    "Junk Pit": [],
}


def has_door(door: str, state: CollectionState, world: DoorSalesmanWorld, include_repairs: bool = None) -> bool:
    if include_repairs is None:
        include_repairs = False

    if state.has(door, world.player):
        return True

    if include_repairs:
        for i in repairs_to:
            if repairs_to[i] == door:
                if i in repair_requirements:
                    # TODO currently cost won't be consistent if this is called inside of can_meet_cost
                    if state.has_all([i] + repair_requirements[i] + ["Toolkit"], world.player) and can_meet_cost(repair_costs[i], state, world, False):
                        return True
                else:
                    if state.has(i, world.player):
                        return True
    return False


def can_repair_door(door: str, state: CollectionState, world: DoorSalesmanWorld) -> bool:
    if not door in repair_requirements:
        return True
    return state.has_all(repair_requirements[door] + ["Toolkit"], world.player)


def can_repair_all_variants(door: str, state: CollectionState, world: DoorSalesmanWorld) -> bool:
    for i in repairs_to:
        if repairs_to[i] == door:
            if not can_repair_door(door, state, world):
                return False
    return True


def can_meet_cost(cost: int, state: CollectionState, world: DoorSalesmanWorld, include_repairs: bool = None) -> bool:
    if include_repairs is None:
        include_repairs = True
    money = 0
    for area in area_sells:
        if not can_access_area(area, state, world):
            continue
        for door in area_sells[area]:
            # TODO include has_door price here
            if has_door(door, state, world, include_repairs):
                if can_repair_all_variants(door, state, world):
                    return True
                else:
                    money += door_prices[door] * state.prog_items[world.player][door]
                    if money >= cost:
                        return True

    return False


def can_access_area(area: str, state: CollectionState, world: DoorSalesmanWorld) -> bool:
    if area in ["Warehouse", "Shrimpville", "Fancytown"]:
        return True
    elif area == "Industrial Zone":
        return state.has_all(["Toolkit", "Glassworking"], world.player)
    else:
        for i in NEIGHBORHOOD_CONNECTIONS:
            if area in NEIGHBORHOOD_CONNECTIONS[i]:
                return can_access_area(i, state, world) and state.has(area + " neighborhood unlock", world.player)
    return False


def can_get_shop_item(item: str, state: CollectionState, world: DoorSalesmanWorld) -> bool:
    if not can_access_area(item.split(" shop item ")[0], state, world):
        return False
    if not item in shop_costs:
        return False
    if shop_costs[item] >= 90:
        return True
    return can_meet_cost(shop_costs[item], state, world)


def can_complete_npc(npc: str, state: CollectionState, world: DoorSalesmanWorld) -> bool:
    lives = ""
    for i in neighborhood_populations:
        if npc in neighborhood_populations[i]:
            lives = i
            break
    if not can_access_area(lives, state, world):
        return False
    for i in npc_wants[npc]:
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
    for shop_item in shop_costs:
        set_rule(world.get_location(shop_item), lambda state, current = shop_item: can_get_shop_item(current, state, world))
    for npc in npc_wants:
        set_rule(world.get_location(npc + " Old Door"), lambda state, current = npc: can_complete_npc(current, state, world))
    for unlock in unlock_npcs:
        set_rule(world.get_location(unlock + " neighborhood unlock"), lambda state, current = unlock: can_complete_npc(unlock_npcs[current], state, world))


def set_completion_condition(world: DoorSalesmanWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Coldington neighborhood unlock", world.player)
