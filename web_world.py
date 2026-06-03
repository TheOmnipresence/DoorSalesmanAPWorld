from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

from .options import option_groups, option_presets


# For our game to display correctly on the website, we need to define a WebWorld subclass.
class DoorSalesmanWebWorld(WebWorld):
    game = "Door to Door Door Salesman"

    # You can choose between dirt, grass, grassFlowers, ice, jungle, ocean, partyTime, and stone.
    theme = "partyTime"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Door to Door Door Salesman for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["InterestedSC2"],
    )

    tutorials = [setup_en]

    option_groups = option_groups
    options_presets = option_presets
