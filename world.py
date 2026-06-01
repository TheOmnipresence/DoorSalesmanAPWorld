from collections.abc import Mapping
from typing import Any

# Imports of base Archipelago modules must be absolute.
from worlds.AutoWorld import World

# Imports of your world's files must be relative.
from . import items, locations, regions, rules, web_world
from . import options as door_salesman_options


class DoorSalesmanWorld(World):
    """
    Door to Door Door Salesman is an economy-based business rougelite about selling people doors.
    """

    game = "Door to Door Door Salesman"

    web = web_world.DoorSalesmanWebWorld()

    options_dataclass = door_salesman_options.DoorSalesmanOptions
    options: door_salesman_options.DoorSalesmanOptions

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Warehouse"


    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)


    def set_rules(self) -> None:
        rules.set_all_rules(self)


    def create_items(self) -> None:
        items.create_all_items(self)

    
    def create_item(self, name: str) -> items.DoorSalesmanItem:
        return items.create_item_with_correct_classification(self, name)

    
    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)


    def fill_slot_data(self) -> Mapping[str, Any]:
        # If you need access to the player's chosen options on the client side, there is a helper for that.
        return self.options.as_dict(
            "death_link", "death_link_amnesty",
        )
