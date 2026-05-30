from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle


@dataclass
class DoorSalesmanOptions(PerGameCommonOptions):
    pass
    # hard_mode: HardMode
    # hammer: Hammer
    # extra_starting_chest: ExtraStartingChest
    # start_with_one_confetti_cannon: StartWithOneConfettiCannon
    # trap_chance: TrapChance
    # confetti_explosiveness: ConfettiExplosiveness
    # player_sprite: PlayerSprite


# If we want to group our options by similar type, we can do so as well. This looks nice on the website.
option_groups = []

# Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
option_presets = {}
