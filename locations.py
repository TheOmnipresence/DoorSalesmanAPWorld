from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from BaseClasses import ItemClassification, Location

from .rules import neighborhood_populations, unlock_npcs

if TYPE_CHECKING:
    from .world import DoorSalesmanWorld


def map_to_dict(array: list, method: Callable) -> dict:
    result = {}
    for i in array:
        result[i] = method(i)
    return result


SHOP_LOCATIONS = [
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
    "Coldington shop item 1",
    "Industrial Zone shop item 1",
    "Industrial Zone shop item 2",
    "Industrial Zone shop item 3",
    "Industrial Zone shop item 4",
    "Industrial Zone shop item 5",
]
OLD_DOORS = [
    "May Old Door",
    "Doug Old Door",
    "Mr Brown Old Door",
    "Liliana Old Door",
    "Ice Man Old Door",

    "Poshman Old Door",
    "Hole Guy Old Door",
    "Gold Old Door",

    "John Bottom Old Door",
    "John Top Old Door",

    "Dr Lebut Old Door",

    "Jeff Old Door",
]
NEIGHBORHOOD_UNLOCKS = [
    "Mansion Lane neighborhood unlock",
    "Coldington neighborhood unlock",
]

LOCATION_NAME_TO_ID = map_to_dict(SHOP_LOCATIONS, lambda e: SHOP_LOCATIONS.index(e) + 1) | map_to_dict(OLD_DOORS, lambda e: OLD_DOORS.index(e) + 1000) | map_to_dict(NEIGHBORHOOD_UNLOCKS, lambda e: NEIGHBORHOOD_UNLOCKS.index(e) + 2000)


class DoorSalesmanLocation(Location):
    game = "Door to Door Door Salesman"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: DoorSalesmanWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: DoorSalesmanWorld) -> None:
    for i in SHOP_LOCATIONS:
        region = world.get_region(i.split(" shop item ")[0])
        region.locations.append(DoorSalesmanLocation(world.player, i, LOCATION_NAME_TO_ID[i], region))

    for i in neighborhood_populations:
        unlocks = []
        for neighborhood in unlock_npcs:
            if unlock_npcs[neighborhood] in neighborhood_populations[i]:
                unlocks.append(neighborhood + " neighborhood unlock")
        world.get_region(i).add_locations(get_location_names_with_ids(list(map(lambda e: e + " Old Door", neighborhood_populations[i])) + unlocks))

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
