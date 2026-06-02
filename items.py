from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from .locations import NEIGHBORHOOD_UNLOCKS, map_to_dict

if TYPE_CHECKING:
    from .world import DoorSalesmanWorld

# Every item must have a unique integer ID associated with it.
# We will have a lookup from item name to ID here that, in world.py, we will import and bind to the world class.
# Even if an item doesn't exist on specific options, it must be present in this lookup.
DOORS = [
    "Base Door",
    "Knobless Base Door",
    "Plain Door",
    "Scratched Door",
    "Oak Door",
    "Cracked Oak Door",
    "Hole Oak Door",
    "Ripped Screen Door",
    "Screen Door",
    "Ewhs Door",
    "Fractured Ewhs Door",
    "Blue Door",
    "Rough Blue Door",
    "Gold Oak Door",
    "Glass Door",
    "Fractured Glass Door",
    "Mansion Door",
    "Cracked Mansion Door",
    "Steel Door",
    "Wheelless Steel Door",
    "Ice Door",
    "Melted Door",
    "Brick Door",
]

ITEM_NAME_TO_ID = map_to_dict(DOORS, lambda e: DOORS.index(e) + 1) | map_to_dict(NEIGHBORHOOD_UNLOCKS, lambda e: NEIGHBORHOOD_UNLOCKS.index(e) + 2000) | {
    "Day Advance": 1000,

    "Toolkit": 1100,
    "Glassworking": 1101,
    "Welding": 1102,
    "Freezer": 1103,

    # "Knock Power 1": 1200,

    "Warehouse Storage 2": 1300,

    "Truck Bed": 1400,

    "Wheelbarrow": 1500,
}

DOOR_CLASSIFICATIONS = {
    "Base Door": ItemClassification.progression_deprioritized_skip_balancing,
    "Knobless Base Door": ItemClassification.progression_deprioritized_skip_balancing,
    "Plain Door": ItemClassification.progression_deprioritized_skip_balancing,
    "Scratched Door": ItemClassification.progression_deprioritized_skip_balancing,
    "Oak Door": ItemClassification.progression_deprioritized_skip_balancing,
    "Cracked Oak Door": ItemClassification.progression_deprioritized_skip_balancing,
    "Hole Oak Door": ItemClassification.progression_deprioritized_skip_balancing,
    "Ripped Screen Door": ItemClassification.progression_deprioritized_skip_balancing,
    "Screen Door": ItemClassification.progression_deprioritized_skip_balancing,
    "Ewhs Door": ItemClassification.progression_deprioritized_skip_balancing,
    "Fractured Ewhs Door": ItemClassification.progression_deprioritized_skip_balancing,
    "Blue Door": ItemClassification.progression_deprioritized_skip_balancing,
    "Rough Blue Door": ItemClassification.progression_deprioritized_skip_balancing,
    "Gold Oak Door": ItemClassification.progression,
    "Glass Door": ItemClassification.progression_deprioritized_skip_balancing,
    "Fractured Glass Door": ItemClassification.progression_deprioritized_skip_balancing,
    "Mansion Door": ItemClassification.progression_deprioritized_skip_balancing,
    "Cracked Mansion Door": ItemClassification.progression_deprioritized_skip_balancing,
    "Steel Door": ItemClassification.progression_deprioritized_skip_balancing,
    "Wheelless Steel Door": ItemClassification.progression_deprioritized_skip_balancing,
    "Ice Door": ItemClassification.progression,
    "Melted Door": ItemClassification.progression_deprioritized_skip_balancing,
    "Brick Door": ItemClassification.progression,
}

DEFAULT_ITEM_CLASSIFICATIONS = DOOR_CLASSIFICATIONS | map_to_dict(NEIGHBORHOOD_UNLOCKS, lambda e: ItemClassification.progression) | {
    "Day Advance": ItemClassification.filler,

    "Toolkit": ItemClassification.progression,
    "Glassworking": ItemClassification.progression,
    "Welding": ItemClassification.progression,
    "Freezer": ItemClassification.progression,

    "Warehouse Storage 2": ItemClassification.useful,

    "Truck Bed": ItemClassification.useful,

    "Wheelbarrow": ItemClassification.useful,
}

all_door_items = [
    #shop doors
    "Base Door",
    "Base Door",
    "Oak Door",
    "Gold Oak Door",
    "Ewhs Door",
    "Ice Door",
    "Glass Door",
    "Wheelless Steel Door",
    "Brick Door",

    #old doors
    "Scratched Door",
    "Scratched Door",
    "Ripped Screen Door",
    "Rough Blue Door",
    "Melted Door",

    "Cracked Oak Door",
    "Hole Oak Door",
    "Oak Door",

    "Mansion Door",
    "Fractured Glass Door",

    "Melted Door",
]


class DoorSalesmanItem(Item):
    game = "Door to Door Door Salesman"


def get_random_filler_item_name(world: DoorSalesmanWorld) -> str:
    # IMPORTANT: Whenever you need to use a random generator, you must use world.random.
    # This ensures that generating with the same generator seed twice yields the same output.
    # DO NOT use a bare random object from Python's built-in random module.
    # if world.random.randint(0, 99) < world.options.trap_chance:
    #     return "Math Trap"
    # TODO rent trap
    return "Day Advance"


def create_item_with_correct_classification(world: DoorSalesmanWorld, name: str) -> DoorSalesmanItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    return DoorSalesmanItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: DoorSalesmanWorld) -> None:
    itempool: list[Item] = []
    for i in all_door_items + NEIGHBORHOOD_UNLOCKS + ["Toolkit", "Glassworking", "Welding", "Freezer"]:
        itempool.append(world.create_item(i))

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]
    world.multiworld.itempool += itempool

    for i in ["Scratched Door", "Base Door", "Base Door"]:
        world.push_precollected(world.create_item(i))
