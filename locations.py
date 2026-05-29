from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import DoorSalesmanWorld


def map_to_dict(array: list, method: Callable) -> dict:
    result = {}
    for i in array:
        result[i] = method(i)
    return result


NORMAL_LOCATIONS = [
    "Warehouse shop item 1",
    "Warehouse shop item 2",
    "Warehouse shop item 3",
    "Shrimpville shop item 1",
    "Shrimpville shop item 2",
    "Shrimpville shop item 3",
    "Fancytown shop item 1",
    "Fancytown shop item 2",
    "Mansion Lane shop item 1",
    "Mansion Lane shop item 2",
    "Mansion Lane shop item 3",
    "Industrial Zone shop item 1",
    "Industrial Zone shop item 2",
    "Industrial Zone shop item 3",
]

LOCATION_NAME_TO_ID = map_to_dict(NORMAL_LOCATIONS, lambda e: NORMAL_LOCATIONS.index(e))


# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class DoorSalesmanLocation(Location):
    game = "Door to Door Door Salesman"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: DoorSalesmanWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: DoorSalesmanWorld) -> None:
    for i in NORMAL_LOCATIONS:
        region = world.get_region(i.split(" shop item ")[0])
        region.locations.append(DoorSalesmanLocation(world.player, i, LOCATION_NAME_TO_ID[i], region))


    # Locations may exist only if the player enables certain options.
    # In our case, the extra_starting_chest option adds the Bottom Left Extra Chest location.
    # if world.options.extra_starting_chest:
    #     # Once again, it is important to stress that even though the Bottom Left Extra Chest location doesn't always
    #     # exist, it must still always be present in the world's location_name_to_id.
    #     # Whether the location actually exists in the seed is purely determined by whether we create and add it here.
    #     bottom_left_extra_chest = get_location_names_with_ids(["Bottom Left Extra Chest"])
    #     overworld.add_locations(bottom_left_extra_chest, DoorSalesmanLocation)


def create_events(world: DoorSalesmanWorld) -> None:
    pass
