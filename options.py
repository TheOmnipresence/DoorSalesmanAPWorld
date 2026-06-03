from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle


class DeathLink(Toggle):
    """
    Toggles deathlink for this player. The deathlink trigger for this game is when you go bankrupt.
    """

    display_name = "Deathlink"
    default = False


class DeathLinkAmnesty(Range):
    """
    The amount of bankrupts needed to send a deathlink.
    """

    display_name = "Deathlink Amnesty"
    range_start = 1
    range_end = 20
    default = 1


@dataclass
class DoorSalesmanOptions(PerGameCommonOptions):
    death_link: DeathLink
    death_link_amnesty: DeathLinkAmnesty


option_groups = []

option_presets = {
    "default": {
        "death_link": False,
        "death_link_amnesty": 1,
    },
    "deathlink": {
        "death_link": True,
        "death_link_amnesty": 1,
    }
}
