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
area_sells = {
    "Workshop": [],
    "Shrimpville": ["Base Door", "Oak Door", "Screen Door", "Scratched Door", "Plain Door", "Ewhs Door", "Blue Door", "Ice Door"],
    "Fancytown": ["Oak Door", "Gold Oak Door"],
    "Mansion Lane": ["Blue Door", "Mansion Door", "Glass Door"],
    "Coldington": [],
    "Industrial Zone": [],
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


def set_all_rules(world: DoorSalesmanWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: DoorSalesmanWorld) -> None:
   pass


def set_all_location_rules(world: DoorSalesmanWorld) -> None:

    set_rule(world.get_location("Warehouse shop item 1"), lambda state: True)
    set_rule(world.get_location("Warehouse shop item 2"), lambda state: True)
    set_rule(world.get_location("Warehouse shop item 3"), lambda state: True)
    set_rule(world.get_location("Shrimpville shop item 1"), lambda state: True)
    set_rule(world.get_location("Shrimpville shop item 2"), lambda state: True)
    set_rule(world.get_location("Shrimpville shop item 3"), lambda state: can_meet_cost(210, state, world))

    # Location rules work no differently from Entrance rules.
    # Most of our locations are chests that can simply be opened by walking up to them.
    # Thus, their logical requirements are covered by the Entrance rules of the Entrances that were required to
    # reach the region that the chest sits in.
    # However, our two enemies work differently.
    # Entering the room with the enemy is not enough, you also need to have enough combat items to be able to defeat it.
    # So, we need to set requirements on the Locations themselves.
    # Since combat is a bit more complicated, we'll use this chance to cover some advanced access rule concepts.

    # Sometimes, you may want to have different rules depending on the player's chosen options.
    # There is a wrong way to do this, and a right way to do this. Let's do the wrong way first.
    right_room_enemy = world.get_location("Right Room Enemy Drop")

    # DON'T DO THIS!!!!
    set_rule(
        right_room_enemy,
        lambda state: (
            state.has("Sword", world.player)
            and (not world.options.hard_mode or state.has_any(("Shield", "Health Upgrade"), world.player))
        ),
    )
    # DON'T DO THIS!!!!

    # Now, what's actually wrong with this? It works perfectly fine, right?
    # If hard mode disabled, Sword is enough. If hard mode is enabled, we also need a Shield or a Health Upgrade.
    # The access rule we just wrote does this correctly, so what's the problem?
    # The problem is performance.
    # Most of your world code doesn't need to be perfectly performant, since it just runs once per slot.
    # However, access rules in particular are by far the hottest code path in Archipelago.
    # An access rule will potentially be called thousands or even millions of times over the course of one generation.
    # As a result, access rules are the one place where it's really worth putting in some effort to optimize.
    # What's the performance problem here?
    # Every time our access rule is called, it has to evaluate whether world.options.hard_mode is True or False.
    # Wouldn't it be better if in easy mode, the access rule only checked for Sword to begin with?
    # Wouldn't it also be better if in hard mode, it already knew it had to check Shield and Health Upgrade as well?
    # Well, we can achieve this by doing the "if world.options.hard_mode" check outside the set_rule call,
    # and instead having two *different* set_rule calls depending on which case we're in.

    if world.options.hard_mode:
        # If you have multiple conditions, you can obviously chain them via "or" or "and".
        # However, there are also the nice helper functions "state.has_any" and "state.has_all".
        set_rule(
            right_room_enemy,
            lambda state: (
                state.has("Sword", world.player) and state.has_any(("Shield", "Health Upgrade"), world.player)
            ),
        )
    else:
        set_rule(right_room_enemy, lambda state: state.has("Sword", world.player))

    # Another way to chain multiple conditions is via the add_rule function.
    # This makes the access rules a bit slower though, so it should only be used if your structure justifies it.
    # In our case, it's pretty useful because hard mode and easy mode have different requirements.
    final_boss = world.get_location("Final Boss Defeated")

    # For the "known" requirements, it's still better to chain them using a normal "and" condition.
    add_rule(final_boss, lambda state: state.has_all(("Sword", "Shield"), world.player))

    if world.options.hard_mode:
        # You can check for multiple copies of an item by using the optional count parameter of state.has().
        add_rule(final_boss, lambda state: state.has("Health Upgrade", world.player, 2))


def set_completion_condition(world: DoorSalesmanWorld) -> None:
    # Finally, we need to set a completion condition for our world, defining what the player needs to win the game.
    # You can just set a completion condition directly like any other condition, referencing items the player receives:
    world.multiworld.completion_condition[world.player] = lambda state: state.has_all(("Sword", "Shield"), world.player)

    # In our case, we went for the Victory event design pattern (see create_events() in locations.py).
    # So lets undo what we just did, and instead set the completion condition to:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
