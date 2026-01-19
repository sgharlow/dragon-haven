"""
Dragon Haven Cafe - Entry Point
A dragon-raising cafe management simulation game.
"""

import os

from game import Game
from state_manager import StateManager

# Get the directory containing this script (src/)
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the project root (parent of src/)
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)
# Data directory
_DATA_DIR = os.path.join(_PROJECT_ROOT, 'data')

# Import all states
from states.main_menu_state import MainMenuState
from states.settings_state import SettingsState
from states.exploration_mode_state import ExplorationModeState
from states.cafe_mode_state import CafeModeState
from states.inventory_state import InventoryState
from states.recipe_book_state import RecipeBookState
from states.dragon_status_state import DragonStatusState
from states.pause_menu_state import PauseMenuState
from states.save_load_state import SaveLoadState
from states.dragon_naming_state import DragonNamingState

# Initialize managers
from save_manager import get_save_manager
from sound_manager import get_sound_manager
from systems.time_system import get_time_manager
from systems.inventory import get_inventory
from systems.world import get_world_manager
from systems.recipes import get_recipe_manager
from systems.dialogue import get_dialogue_manager
from systems.story import get_story_manager
from entities.story_character import get_character_manager
from game_state import get_game_state_manager
from systems.dragon_manager import get_dragon_manager


def initialize_systems():
    """Initialize all game systems and load data."""
    # Initialize save manager
    save_mgr = get_save_manager()
    save_mgr.initialize()

    # Initialize sound manager
    sound_mgr = get_sound_manager()
    sound_mgr.initialize()

    # Initialize time system
    time_mgr = get_time_manager()

    # Initialize inventory
    inventory = get_inventory()

    # Initialize world/zones
    world_mgr = get_world_manager()

    # Initialize recipe system (recipes loaded from constants.py)
    recipe_mgr = get_recipe_manager()

    # Initialize dialogue system
    dialogue_mgr = get_dialogue_manager()
    dialogue_mgr.load_dialogues_from_directory(os.path.join(_DATA_DIR, 'dialogues'))

    # Initialize story system
    story_mgr = get_story_manager()
    story_mgr.load_events_from_directory(os.path.join(_DATA_DIR, 'events'))

    # Initialize character system
    char_mgr = get_character_manager()
    char_mgr.load_characters_file(os.path.join(_DATA_DIR, 'characters', 'story_characters.json'))

    # Initialize game state manager and enable auto-save
    game_state_mgr = get_game_state_manager()
    game_state_mgr.enable_autosave()

    # Initialize dragon manager
    dragon_mgr = get_dragon_manager()

    # Register dialogue events
    def on_name_dragon_popup():
        """Handle name_dragon_popup dialogue trigger."""
        dragon_mgr.request_naming()

    dialogue_mgr.register_event('name_dragon_popup', on_name_dragon_popup)


def main():
    """Main entry point for Dragon Haven Cafe."""
    # Create the game
    game = Game()

    # Create and register state manager
    state_manager = StateManager()
    game.register_state_manager(state_manager)

    # Initialize all game systems
    initialize_systems()

    # Register all states
    # Menu states
    game.register_state("main_menu", MainMenuState(game))
    game.register_state("settings", SettingsState(game))
    game.register_state("pause_menu", PauseMenuState(game))
    game.register_state("save_load", SaveLoadState(game, mode='save'))

    # Gameplay states
    game.register_state("exploration", ExplorationModeState(game))
    game.register_state("cafe", CafeModeState(game))
    game.register_state("gameplay", ExplorationModeState(game))  # Alias for main menu

    # Popup states (inventory, recipes, dragon status)
    game.register_state("inventory", InventoryState(game))
    game.register_state("recipe_book", RecipeBookState(game))
    game.register_state("dragon_status", DragonStatusState(game))
    game.register_state("dragon_naming", DragonNamingState(game))

    # Set initial state to main menu
    game.set_initial_state("main_menu")

    # Run the game loop
    game.run()


if __name__ == "__main__":
    main()
