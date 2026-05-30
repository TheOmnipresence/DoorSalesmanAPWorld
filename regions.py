from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import DoorSalesmanWorld


neighborhoods = [
    "Warehouse",
    "Shrimpville",
    "Fancytown",
    "Mansion Lane",
    "Coldington",
    "Industrial Zone",
]


def create_and_connect_regions(world: DoorSalesmanWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: DoorSalesmanWorld) -> None:
    for i in neighborhoods:
        world.multiworld.regions.append(Region(i, world.player, world.multiworld))

    # Some regions may only exist if the player enables certain options.
    # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    # if world.options.hammer:
    #     top_middle_room = Region("Top Middle Room", world.player, world.multiworld)
    #     regions.append(top_middle_room)

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    # world.multiworld.regions += regions


def connect_regions(world: DoorSalesmanWorld) -> None:
    # We have regions now, but still need to connect them to each other.
    # But wait, we no longer have access to the region variables we created in create_all_regions()!
    # Luckily, once you've submitted your regions to multiworld.regions,
    # you can get them at any time using world.get_region(...).
    regions = {}
    for i in neighborhoods:
        regions[i] = world.get_region(i)

    regions["Warehouse"].connect(regions["Shrimpville"], lambda state: True)
    regions["Warehouse"].connect(regions["Fancytown"], lambda state: True)
    regions["Fancytown"].connect(regions["Mansion Lane"], lambda state: state.has("Mansion Lane neighborhood unlock", world.player)) #has_door("Gold Door", state, world))
    regions["Shrimpville"].connect(regions["Coldington"], lambda state: state.has("Coldington neighborhood unlock", world.player)) #has_door("Ice Door", state, world))
    regions["Warehouse"].connect(regions["Industrial Zone"], lambda state: state.has_all(["Toolkit", "Glassworking"], world.player))


    # Some Entrances may only exist if the player enables certain options.
    # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    # In this case, we previously created an extra "Top Middle Room" region that we now need to connect to Overworld.
    # if world.options.hammer:
    #     top_middle_room = world.get_region("Top Middle Room")
    #     overworld.connect(top_middle_room, "Overworld to Top Middle Room")
